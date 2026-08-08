from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.repositories.base import BaseRepository
from backend.models.audit import AuditLog


class AuditRepository(BaseRepository[AuditLog]):
    def __init__(self):
        super().__init__(AuditLog)

    def get_by_investigation_id(self, db: Session, investigation_id: str) -> List[AuditLog]:
        return db.query(AuditLog).filter(
            AuditLog.investigation_id == investigation_id
        ).order_by(desc(AuditLog.created_at)).all()

    def get_latest_audit_logs(self, db: Session, limit: int = 50) -> List[AuditLog]:
        return db.query(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit).all()
