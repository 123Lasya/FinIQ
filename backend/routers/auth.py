from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.auth_service import AuthService
from backend.schemas.auth import LoginRequest, LoginResponse
from backend.utils.deps import get_current_active_user
from backend.models.user import User
from backend.utils.response import api_response

router = APIRouter(prefix="/auth", tags=["Employee Authentication"])
auth_service = AuthService()


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Employee Login endpoint issuing JWT Token."""
    res = auth_service.login_employee(db, payload.email, payload.password)
    return api_response(
        data=res,
        message="Employee login successful.",
        status_code=status.HTTP_200_OK
    )


@router.post("/logout")
def logout(current_user: User = Depends(get_current_active_user)):
    """Employee Logout endpoint."""
    return api_response(
        data=None,
        message="Employee logged out successfully.",
        status_code=status.HTTP_200_OK
    )


@router.get("/me")
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    """Retrieves authenticated Employee profile."""
    user_data = {
        "employee_id": current_user.employee_id,
        "email": current_user.email,
        "first_name": getattr(current_user, "first_name", "Employee"),
        "last_name": getattr(current_user, "last_name", "User"),
        "role": current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role),
        "department": getattr(current_user, "department", "Operations"),
        "is_active": current_user.is_active
    }
    return api_response(
        data=user_data,
        message="Current employee profile retrieved successfully.",
        status_code=status.HTTP_200_OK
    )
