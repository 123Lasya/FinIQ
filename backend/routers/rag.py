import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.schemas.rag import SearchQuery, SearchResult
from backend.services.rag_service import RAGService

router = APIRouter(prefix="/rag", tags=["RAG & Knowledge Base"])
rag_service = RAGService()


@router.post("/upload")
def upload_policy_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Uploads a PDF, DOCX, or TXT enterprise policy document into the ChromaDB RAG vector store."""
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = rag_service.ingest_document_file(temp_path, file.filename)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process policy document: {str(e)}"
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/search", response_model=List[SearchResult])
def search_policy_knowledge_base(
    payload: SearchQuery,
    current_user: User = Depends(get_current_active_user)
):
    """Queries ChromaDB vector store for relevant policy chunks."""
    results = rag_service.search_policies(payload.query, top_k=payload.top_k)
    output = []
    for r in results:
        output.append(SearchResult(
            document_id=r.get("document_id", ""),
            content=r.get("content", ""),
            metadata=r.get("metadata", {}),
            score=r.get("score", 0.0)
        ))
    return output
