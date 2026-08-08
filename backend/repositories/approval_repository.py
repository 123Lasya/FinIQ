from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.repositories.base import BaseRepository
from backend.models.approval import Approval
from backend.models.enums import ApprovalStatus


class ApprovalRepository(BaseRepository[Approval]):
    def __init__(self):
        super().__init__(Approval)

    def get_by_approval_id(self, db: Session, approval_id: str) -> Optional[Approval]:
        return db.query(Approval).filter(Approval.approval_id == approval_id).first()

    def get_by_investigation_id(self, db: Session, investigation_id: str) -> Optional[Approval]:
        return db.query(Approval).filter(Approval.investigation_id == investigation_id).first()

    def list_approvals(self, db: Session, status: Optional[ApprovalStatus] = None) -> List[Approval]:
        query = db.query(Approval)
        if status:
            query = query.filter(Approval.status == status)
        return query.order_by(desc(Approval.created_at)).all()
