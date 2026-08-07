from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.schemas.investigation import (
    InvestigationCreate,
    InvestigationResponse,
    InvestigationDetailResponse,
    ApprovalActionRequest
)
from backend.schemas.agent import AgentStepLog
from backend.services.investigation_service import InvestigationService

router = APIRouter(prefix="/investigations", tags=["Investigation Tokens & Workflow"])
service = InvestigationService()


@router.post("/", response_model=InvestigationResponse, status_code=status.HTTP_201_CREATED)
def create_investigation_token(
    payload: InvestigationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Creates a new Investigation Token for customer complaint intake."""
    return service.create_investigation_token(db, payload)


@router.get("/", response_model=List[InvestigationResponse])
def list_investigations(
    status: Optional[str] = Query(None, description="Filter by status (PENDING, IN_PROGRESS, AUTO_EXECUTED, REQUIRES_HUMAN_APPROVAL, APPROVED, REJECTED)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lists investigation tokens with optional status filtering."""
    return service.list_investigations(db, status=status)


@router.get("/queue", response_model=List[InvestigationResponse])
def get_incoming_queue(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves incoming queue awaiting AI activation or Human Approval."""
    pending = service.list_investigations(db, status="PENDING")
    requires_approval = service.list_investigations(db, status="REQUIRES_HUMAN_APPROVAL")
    return pending + requires_approval


@router.get("/{token_id}", response_model=InvestigationDetailResponse)
def get_investigation_details(
    token_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Gets detailed state and multi-agent logs for a specific Investigation Token."""
    inv = service.get_investigation_by_token(db, token_id)
    if not inv:
        raise HTTPException(status_code=404, detail=f"Token {token_id} not found")

    logs = service.get_investigation_logs(db, token_id)
    detail = InvestigationDetailResponse.model_validate(inv)
    detail.agent_logs = logs
    return detail


@router.post("/{token_id}/activate", response_model=InvestigationDetailResponse)
def activate_investigation_pipeline(
    token_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Activates the multi-agent AI pipeline for an Investigation Token."""
    inv = service.activate_investigation(db, token_id, current_user.employee_id)
    logs = service.get_investigation_logs(db, token_id)
    detail = InvestigationDetailResponse.model_validate(inv)
    detail.agent_logs = logs
    return detail


@router.post("/{token_id}/approval", response_model=InvestigationDetailResponse)
def submit_human_approval(
    token_id: str,
    action_data: ApprovalActionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Human-in-the-loop endpoint for Employee to APPROVE or REJECT flagged cases."""
    inv = service.process_human_approval(db, token_id, action_data, current_user.employee_id)
    logs = service.get_investigation_logs(db, token_id)
    detail = InvestigationDetailResponse.model_validate(inv)
    detail.agent_logs = logs
    return detail


@router.get("/{token_id}/logs", response_model=List[AgentStepLog])
def get_investigation_agent_logs(
    token_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves step-by-step agent telemetry logs for an Investigation Token."""
    return service.get_investigation_logs(db, token_id)
