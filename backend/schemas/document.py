from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from backend.models.enums import EmbeddingStatus


class KnowledgeDocumentResponse(BaseModel):
    document_id: str
    title: str
    filename: str
    category: str
    file_path: str
    chunk_count: int
    embedding_status: EmbeddingStatus
    uploaded_by: str
    uploaded_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentChunkResponse(BaseModel):
    chunk_id: str
    document_id: str
    chunk_text: str
    page_number: Optional[int] = None
    embedding_id: Optional[str] = None

    class Config:
        from_attributes = True


class RetrievalChunkResult(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    filename: str
    category: str
    page_number: Optional[int] = None
    chunk_text: str
    similarity_score: float
    metadata: Dict[str, Any]
