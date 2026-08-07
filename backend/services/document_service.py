import os
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.models.document import KnowledgeDocument, DocumentChunk
from backend.models.enums import EmbeddingStatus
from backend.rag.parsers import PDFParser, DOCXParser, TXTParser
from backend.rag.chunker import ChunkingService
from backend.rag.vector_store import VectorStoreService
from backend.utils.logger import get_logger
from backend.utils.exceptions import ResourceNotFoundException

logger = get_logger("finpilot.services.document")


class DocumentUploadService:
    """Service handling Knowledge Base document parsing, chunking, MySQL metadata storage, and ChromaDB vector indexing."""

    def __init__(self):
        self.chunker = ChunkingService()
        self.vector_store = VectorStoreService()

    def process_and_index_document(
        self,
        db: Session,
        file_path: str,
        title: str,
        filename: str,
        category: str,
        uploaded_by_employee_id: str
    ) -> KnowledgeDocument:
        """Parses file (PDF/DOCX/TXT), chunks text, persists metadata in MySQL, and indexes vectors into ChromaDB."""
        logger.info(f"Processing document for upload & indexing: {filename} ({category})")

        # 1. Parse File Content based on extension
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".pdf":
            pages = PDFParser.parse_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            pages = DOCXParser.parse_docx(file_path)
        else:
            pages = TXTParser.parse_txt(file_path)

        # 2. Save KnowledgeDocument Record in MySQL
        doc = KnowledgeDocument(
            title=title,
            filename=filename,
            category=category,
            file_path=file_path,
            chunk_count=0,
            embedding_status=EmbeddingStatus.PROCESSING,
            uploaded_by=uploaded_by_employee_id
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        try:
            # 3. Chunk Document Pages
            chunks = self.chunker.chunk_pages(pages, document_id=doc.document_id)

            # 4. Save Chunks into MySQL
            db_chunks = []
            metadatas = []
            for c in chunks:
                chunk_obj = DocumentChunk(
                    document_id=doc.document_id,
                    chunk_text=c["chunk_text"],
                    page_number=c["page_number"]
                )
                db.add(chunk_obj)
                db.flush()

                c["chunk_id"] = chunk_obj.chunk_id
                chunk_obj.embedding_id = f"emb-{chunk_obj.chunk_id}"
                db_chunks.append(chunk_obj)

                metadatas.append({
                    "document_id": doc.document_id,
                    "chunk_id": chunk_obj.chunk_id,
                    "title": doc.title,
                    "filename": doc.filename,
                    "category": doc.category,
                    "page_number": c["page_number"]
                })

            db.commit()

            # 5. Index Embeddings into ChromaDB
            self.vector_store.upsert_chunks(chunks=chunks, metadatas=metadatas)

            doc.chunk_count = len(chunks)
            doc.embedding_status = EmbeddingStatus.COMPLETED
            db.commit()
            db.refresh(doc)
            logger.info(f"Successfully processed document '{filename}': {len(chunks)} chunks indexed.")
            return doc

        except Exception as e:
            logger.error(f"Error during document indexing for '{filename}': {e}")
            doc.embedding_status = EmbeddingStatus.FAILED
            db.commit()
            raise e

    @staticmethod
    def list_documents(db: Session) -> List[KnowledgeDocument]:
        return db.query(KnowledgeDocument).all()

    @staticmethod
    def get_document_by_id(db: Session, document_id: str) -> KnowledgeDocument:
        doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.document_id == document_id).first()
        if not doc:
            raise ResourceNotFoundException("KnowledgeDocument", document_id)
        return doc
