from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.models.audit import AuditLog
from backend.schemas.agent import AgentStepLog

router = APIRouter(prefix="/audit", tags=["Immutable Compliance Audit Logs"])


@router.get("/logs", response_model=List[AgentStepLog])
def list_system_audit_logs(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lists recent system audit trail logs across all investigation tokens."""
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()
    out = []
    for l in logs:
        out.append(AgentStepLog(
            agent_name=l.agent_name,
            step_number=l.step_number,
            action=l.action,
            input_summary=l.input_payload[:120] if l.input_payload else "",
            output_summary=l.output_payload[:120] if l.output_payload else "",
            execution_time_ms=l.execution_time_ms,
            hash_signature=l.hash_signature,
            created_at=l.created_at
        ))
    return out


@router.get("/investigation/{token_id}", response_model=List[AgentStepLog])
def get_token_audit_trail(
    token_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves full immutable audit trail for a specific investigation token."""
    logs = db.query(AuditLog).filter(AuditLog.investigation_token_id == token_id).order_by(AuditLog.step_number.asc()).all()
    out = []
    for l in logs:
        out.append(AgentStepLog(
            agent_name=l.agent_name,
            step_number=l.step_number,
            action=l.action,
            input_summary=l.input_payload[:120] if l.input_payload else "",
            output_summary=l.output_payload[:120] if l.output_payload else "",
            execution_time_ms=l.execution_time_ms,
            hash_signature=l.hash_signature,
            created_at=l.created_at
        ))
    return out
