from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from backend.models.enums import EmployeeRole


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str = "Financial Operations"
    role: EmployeeRole = EmployeeRole.OPERATIONS_EXEC


class EmployeeCreate(EmployeeBase):
    password: str


class EmployeeResponse(EmployeeBase):
    employee_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
