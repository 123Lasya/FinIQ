from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.user import User
from backend.schemas.auth import LoginRequest, Token
from backend.utils.jwt import verify_password, create_access_token


class AuthService:
    """Service handling Employee authentication logic."""

    @staticmethod
    def authenticate_employee(db: Session, login_data: LoginRequest) -> Token:
        user = db.query(User).filter(User.employee_id == login_data.employee_id).first()
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid employee credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee account disabled"
            )

        token_data = {
            "sub": user.employee_id,
            "employee_id": user.employee_id,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name
        }
        access_token = create_access_token(data=token_data)

        return Token(
            access_token=access_token,
            token_type="bearer",
            employee_id=user.employee_id,
            email=user.email,
            role=user.role,
            full_name=user.full_name
        )
