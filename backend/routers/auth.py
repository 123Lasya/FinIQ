from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.auth import LoginRequest, Token, UserRead
from backend.services.auth_service import AuthService
from backend.utils.deps import get_current_active_user
from backend.models.user import User

router = APIRouter(prefix="/auth", tags=["Employee Authentication"])


@router.post("/login", response_model=Token)
def employee_login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Employee Login endpoint delivering JWT Access Token."""
    return AuthService.authenticate_employee(db, login_data)


@router.get("/me", response_model=UserRead)
def get_authenticated_employee(
    current_user: User = Depends(get_current_active_user)
):
    """Returns currently authenticated Employee user profile."""
    return current_user
