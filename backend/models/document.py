from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.database import Base, TimestampMixin
from backend.models.enums import EmbeddingStatus
from backend.utils.uuid_utils import generate_uuid


class KnowledgeDocument(Base, TimestampMixin):
    __tablename__ = "knowledge_documents"

    document_id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(150), nullable=False)
    filename = Column(String(150), nullable=False)
    category = Column(String(80), nullable=False, default="POLICY")
    file_path = Column(String(255), nullable=False)
    chunk_count = Column(Integer, default=0, nullable=False)
    embedding_status = Column(SQLEnum(EmbeddingStatus), nullable=False, default=EmbeddingStatus.PENDING)
    
    uploaded_by = Column(String(36), ForeignKey("employees.employee_id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    uploader = relationship("Employee", back_populates="uploaded_documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base, TimestampMixin):
    __tablename__ = "document_chunks"

    chunk_id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("knowledge_documents.document_id"), nullable=False, index=True)
    chunk_text = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)
    embedding_id = Column(String(120), nullable=True, index=True)

    # Relationships
    document = relationship("KnowledgeDocument", back_populates="chunks")
