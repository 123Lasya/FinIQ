from typing import List, Optional
from sqlalchemy.orm import Session
from backend.repositories.base import BaseRepository
from backend.models.document import KnowledgeDocument


class DocumentRepository(BaseRepository[KnowledgeDocument]):
    def __init__(self):
        super().__init__(KnowledgeDocument)

    def get_by_document_id(self, db: Session, document_id: str) -> Optional[KnowledgeDocument]:
        return db.query(KnowledgeDocument).filter(KnowledgeDocument.document_id == document_id).first()

    def list_documents(self, db: Session) -> List[KnowledgeDocument]:
        return db.query(KnowledgeDocument).order_by(KnowledgeDocument.created_at.desc()).all()
