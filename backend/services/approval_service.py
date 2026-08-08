from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from backend.repositories.approval_repository import ApprovalRepository
from backend.repositories.investigation_repository import InvestigationRepository
from backend.models.enums import ApprovalStatus, InvestigationStatus
from backend.utils.exceptions import ResourceNotFoundException
from backend.logging import logger


class ApprovalService:
    """Service layer managing human approval queue operations."""

    def __init__(self):
        self.approval_repo = ApprovalRepository()
        self.inv_repo = InvestigationRepository()

    def get_approval_queue(self, db: Session) -> List[Dict[str, Any]]:
        approvals = self.approval_repo.list_approvals(db, status=ApprovalStatus.PENDING)
        result = []
        for app in approvals:
            inv = self.inv_repo.get_by_investigation_id(db, app.investigation_id)
            result.append({
                "approval_id": app.approval_id,
                "investigation_id": app.investigation_id,
                "token_id": inv.token_id if inv else "TOK_UNKNOWN",
                "customer_id": inv.customer_id if inv else "",
                "title": inv.title if inv else "Pending Dispute Approval",
                "dispute_amount": getattr(inv, "dispute_amount", 0.0) or 0.0,
                "issue_type": inv.issue_type.value if inv and hasattr(inv.issue_type, "value") else "DISPUTE",
                "status": app.status.value,
                "reason": app.reason,
                "created_at": app.created_at.isoformat() + "Z"
            })
        return result

    def get_approval_detail(self, db: Session, approval_id: str) -> Dict[str, Any]:
        app = self.approval_repo.get_by_approval_id(db, approval_id)
        if not app:
            raise ResourceNotFoundException("Approval Record", approval_id)

        inv = self.inv_repo.get_by_investigation_id(db, app.investigation_id)
        logs = self.inv_repo.get_execution_logs(db, app.investigation_id) if inv else []

        return {
            "approval_id": app.approval_id,
            "investigation_id": app.investigation_id,
            "token_id": inv.token_id if inv else "",
            "customer_id": inv.customer_id if inv else "",
            "title": inv.title if inv else "",
            "description": inv.description if inv else "",
            "recommended_decision": inv.final_decision if inv else "FULL_REFUND",
            "decision_type": inv.decision_type if inv else "PROVISIONAL_CREDIT",
            "status": app.status.value,
            "reason": app.reason,
            "agent_logs": [
                {
                    "agent_name": log.agent_name,
                    "status": log.status.value,
                    "execution_time": log.execution_time,
                    "confidence": log.confidence,
                    "completed_at": log.completed_at.isoformat() + "Z" if log.completed_at else None
                } for log in logs
            ],
            "reviewed_at": app.reviewed_at.isoformat() + "Z"
        }

    def approve_investigation(self, db: Session, approval_id: str, reviewer_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        app = self.approval_repo.get_by_approval_id(db, approval_id)
        if not app:
            raise ResourceNotFoundException("Approval Record", approval_id)

        app.status = ApprovalStatus.APPROVED
        app.reviewed_by = reviewer_id
        app.reviewed_at = datetime.utcnow()
        if notes:
            app.reason = f"Approved by employee: {notes}"

        inv = self.inv_repo.get_by_investigation_id(db, app.investigation_id)
        if inv:
            inv.status = InvestigationStatus.APPROVED
            inv.completed_at = datetime.utcnow()

        db.commit()
        logger.info(f"[ApprovalService] Approval {approval_id} APPROVED by employee {reviewer_id}")
        return self.get_approval_detail(db, approval_id)

    def reject_investigation(self, db: Session, approval_id: str, reviewer_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        app = self.approval_repo.get_by_approval_id(db, approval_id)
        if not app:
            raise ResourceNotFoundException("Approval Record", approval_id)

        app.status = ApprovalStatus.REJECTED
        app.reviewed_by = reviewer_id
        app.reviewed_at = datetime.utcnow()
        if notes:
            app.reason = f"Rejected by employee: {notes}"

        inv = self.inv_repo.get_by_investigation_id(db, app.investigation_id)
        if inv:
            inv.status = InvestigationStatus.REJECTED
            inv.completed_at = datetime.utcnow()

        db.commit()
        logger.info(f"[ApprovalService] Approval {approval_id} REJECTED by employee {reviewer_id}")
        return self.get_approval_detail(db, approval_id)
