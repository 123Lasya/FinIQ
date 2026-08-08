from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.services.approval_service import ApprovalService
from backend.utils.response import api_response

router = APIRouter(prefix="/approvals", tags=["Human-in-the-Loop Approvals Queue"])
approval_service = ApprovalService()


@router.get("")
@router.get("/")
def get_approval_queue(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves list of disputes awaiting human employee approval."""
    queue = approval_service.get_approval_queue(db)
    return api_response(
        data=queue,
        message=f"Retrieved {len(queue)} pending human approval items.",
        status_code=status.HTTP_200_OK
    )


@router.get("/{id}")
def get_approval_detail(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Gets detailed state and multi-agent reasoning for an approval item."""
    detail = approval_service.get_approval_detail(db, id)
    return api_response(
        data=detail,
        message="Approval item details retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.post("/{id}/approve")
def approve_item(
    id: str,
    payload: Dict[str, Any] = Body(default={}),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Human Operations Officer approves a flagged investigation."""
    notes = payload.get("notes") or payload.get("reason")
    res = approval_service.approve_investigation(db, id, current_user.employee_id, notes=notes)
    return api_response(
        data=res,
        message=f"Investigation approval {id} APPROVED by user.",
        status_code=status.HTTP_200_OK
    )


@router.post("/{id}/reject")
def reject_item(
    id: str,
    payload: Dict[str, Any] = Body(default={}),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Human Operations Officer rejects a flagged investigation."""
    notes = payload.get("notes") or payload.get("reason")
    res = approval_service.reject_investigation(db, id, current_user.employee_id, notes=notes)
    return api_response(
        data=res,
        message=f"Investigation approval {id} REJECTED by user.",
        status_code=status.HTTP_200_OK
    )
