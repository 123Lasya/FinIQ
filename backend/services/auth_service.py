from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models.employee import Employee
from backend.schemas.auth import LoginRequest, Token
from backend.utils.jwt import verify_password, create_access_token


class AuthService:
    """Service handling Employee JWT authentication logic."""

    @staticmethod
    def login_employee(db: Session, identifier: str, password: str) -> Token:
        emp = db.query(Employee).filter(
            (Employee.email == identifier) | (Employee.employee_id == identifier)
        ).first()

        if not emp or not verify_password(password, emp.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid employee credentials (email/ID or password incorrect).",
                headers={"WWW-Authenticate": "Bearer"},
            )

        role_str = emp.role.value if hasattr(emp.role, "value") else str(emp.role)

        token_data = {
            "sub": emp.employee_id,
            "employee_id": emp.employee_id,
            "email": emp.email,
            "role": role_str,
            "full_name": emp.name
        }
        access_token = create_access_token(data=token_data)

        return Token(
            access_token=access_token,
            token_type="bearer",
            employee_id=emp.employee_id,
            email=emp.email,
            role=role_str,
            full_name=emp.name
        )

    @staticmethod
    def authenticate_employee(db: Session, login_data: LoginRequest) -> Token:
        identifier = login_data.email or login_data.employee_id or ""
        return AuthService.login_employee(db, identifier, login_data.password)
