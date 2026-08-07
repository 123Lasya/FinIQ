from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.employee import Employee
from backend.schemas.employee import EmployeeCreate
from backend.utils.security import hash_password, verify_password
from backend.utils.exceptions import ResourceNotFoundException, AuthenticationException


class EmployeeService:
    """Service layer for Employee account operations."""

    @staticmethod
    def get_by_id(db: Session, employee_id: str) -> Employee:
        emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
        if not emp:
            raise ResourceNotFoundException("Employee", employee_id)
        return emp

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.email == email).first()

    @staticmethod
    def create_employee(db: Session, payload: EmployeeCreate) -> Employee:
        emp = Employee(
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password),
            department=payload.department,
            role=payload.role
        )
        db.add(emp)
        db.commit()
        db.refresh(emp)
        return emp

    @staticmethod
    def list_employees(db: Session) -> List[Employee]:
        return db.query(Employee).all()
