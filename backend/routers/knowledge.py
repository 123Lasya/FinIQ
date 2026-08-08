import os
import shutil
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.services.document_service import DocumentUploadService
from backend.rag.retrieval_service import KnowledgeRetrievalService
from backend.repositories.document_repository import DocumentRepository
from backend.utils.response import api_response
from backend.utils.exceptions import ResourceNotFoundException

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base & RAG Engine"])
doc_service = DocumentUploadService()
retrieval_service = KnowledgeRetrievalService()
doc_repo = DocumentRepository()

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    category: str = Form("POLICY"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Uploads PDF/DOCX/TXT policy document, chunks text, and indexes vectors into ChromaDB."""
    filename = file.filename or "uploaded_document.pdf"
    doc_title = title or os.path.splitext(filename)[0]

    save_path = os.path.join(UPLOAD_DIR, filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        doc = doc_service.process_and_index_document(
            db=db,
            file_path=save_path,
            title=doc_title,
            filename=filename,
            category=category,
            uploaded_by_employee_id=current_user.employee_id
        )

        doc_data = {
            "document_id": doc.document_id,
            "title": doc.title,
            "filename": doc.filename,
            "category": doc.category,
            "chunk_count": doc.chunk_count,
            "embedding_status": doc.embedding_status.value if hasattr(doc.embedding_status, "value") else str(doc.embedding_status),
            "created_at": doc.created_at.isoformat() + "Z"
        }

        return api_response(
            data=doc_data,
            message=f"Document '{filename}' uploaded and indexed successfully into RAG ChromaDB.",
            status_code=status.HTTP_201_CREATED
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Failed to process document upload: {err}")


@router.get("/documents")
def list_knowledge_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lists all knowledge base policy documents."""
    docs = doc_repo.list_documents(db)
    result = [
        {
            "document_id": d.document_id,
            "title": d.title,
            "filename": d.filename,
            "category": d.category,
            "chunk_count": d.chunk_count,
            "embedding_status": d.embedding_status.value if hasattr(d.embedding_status, "value") else str(d.embedding_status),
            "created_at": d.created_at.isoformat() + "Z"
        } for d in docs
    ]

    return api_response(
        data=result,
        message=f"Retrieved {len(result)} knowledge documents.",
        status_code=status.HTTP_200_OK
    )


@router.delete("/{id}")
def delete_knowledge_document(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Deletes a document record and metadata from knowledge base."""
    success = doc_repo.delete(db, id)
    if not success:
        raise ResourceNotFoundException("Knowledge Document", id)

    return api_response(
        data={"document_id": id},
        message=f"Document {id} deleted successfully.",
        status_code=status.HTTP_200_OK
    )


@router.post("/reindex")
def reindex_knowledge_base(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Reindexes all knowledge base documents into ChromaDB vector store."""
    docs = doc_repo.list_documents(db)
    reindexed_count = 0
    for doc in docs:
        if os.path.exists(doc.file_path):
            try:
                doc_service.process_and_index_document(
                    db=db,
                    file_path=doc.file_path,
                    title=doc.title,
                    filename=doc.filename,
                    category=doc.category,
                    uploaded_by_employee_id=doc.uploaded_by
                )
                reindexed_count += 1
            except Exception:
                pass

    return api_response(
        data={"reindexed_documents": reindexed_count},
        message=f"Reindexed {reindexed_count} knowledge documents into ChromaDB vector store.",
        status_code=status.HTTP_200_OK
    )


@router.get("/search")
def search_knowledge_base(
    q: str = Query(..., description="Query string for semantic vector search"),
    top_k: int = Query(5, description="Number of policy chunks to retrieve"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Performs semantic similarity search over Knowledge Base ChromaDB vector store."""
    chunks = retrieval_service.retrieve_relevant_knowledge(query=q, db=db, top_k=top_k)
    result = [
        {
            "chunk_id": c.chunk_id,
            "document_id": c.document_id,
            "document_title": c.document_title,
            "filename": c.filename,
            "category": c.category,
            "page_number": c.page_number,
            "chunk_text": c.chunk_text,
            "similarity_score": round(c.similarity_score, 4)
        } for c in chunks
    ]

    return api_response(
        data=result,
        message=f"Found {len(result)} matching knowledge policy chunks.",
        status_code=status.HTTP_200_OK
    )
