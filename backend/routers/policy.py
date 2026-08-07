from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.schemas.policy import PolicySchema, PolicyCheckResult
from backend.services.policy_service import PolicyService

router = APIRouter(prefix="/policies", tags=["Compliance Policy Management"])


@router.get("/", response_model=List[PolicySchema])
def list_policies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lists configured compliance policies."""
    return PolicyService.get_all_policies(db)


@router.post("/", response_model=PolicySchema, status_code=status.HTTP_201_CREATED)
def create_policy(
    payload: PolicySchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Creates a new enterprise compliance policy rule."""
    return PolicyService.create_policy(db, payload)


@router.get("/evaluate/{amount}", response_model=PolicyCheckResult)
def evaluate_dispute_amount(
    amount: float,
    current_user: User = Depends(get_current_active_user)
):
    """Evaluates whether a given dispute amount requires human approval or violates policy."""
    return PolicyService.evaluate_amount_compliance(amount)
