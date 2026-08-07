from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.models.investigation import Investigation

router = APIRouter(prefix="/analytics", tags=["Dashboard Operations Analytics"])


@router.get("/dashboard", response_model=Dict[str, Any])
def get_dashboard_operational_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves high-level dashboard telemetry for Employee Operations View."""
    total_tokens = db.query(Investigation).count()
    pending = db.query(Investigation).filter(Investigation.status == "PENDING").count()
    in_progress = db.query(Investigation).filter(Investigation.status == "IN_PROGRESS").count()
    auto_executed = db.query(Investigation).filter(Investigation.status == "AUTO_EXECUTED").count()
    human_approval_required = db.query(Investigation).filter(Investigation.status == "REQUIRES_HUMAN_APPROVAL").count()
    approved = db.query(Investigation).filter(Investigation.status == "APPROVED").count()
    rejected = db.query(Investigation).filter(Investigation.status == "REJECTED").count()

    total_refund_sum = db.query(func.sum(Investigation.dispute_amount)).filter(
        Investigation.status.in_(["AUTO_EXECUTED", "APPROVED"])
    ).scalar() or 0.0

    automation_rate = round((auto_executed / total_tokens * 100.0), 1) if total_tokens > 0 else 0.0

    return {
        "total_investigation_tokens": total_tokens,
        "pending_activation": pending,
        "in_progress": in_progress,
        "auto_executed": auto_executed,
        "human_approval_required": human_approval_required,
        "approved_by_human": approved,
        "rejected_by_human": rejected,
        "total_refunded_amount_inr": float(total_refund_sum),
        "autonomous_execution_rate_percentage": automation_rate
    }
