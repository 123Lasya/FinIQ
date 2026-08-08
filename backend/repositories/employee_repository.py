from typing import Optional
from sqlalchemy.orm import Session
from backend.repositories.base import BaseRepository
from backend.models.employee import Employee


class EmployeeRepository(BaseRepository[Employee]):
    def __init__(self):
        super().__init__(Employee)

    def get_by_email(self, db: Session, email: str) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.email == email).first()

    def get_by_employee_id(self, db: Session, employee_id: str) -> Optional[Employee]:
        return db.query(Employee).filter(Employee.employee_id == employee_id).first()
