from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    employee_id: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    employee_id: str
    email: str
    role: str
    full_name: str


class TokenData(BaseModel):
    employee_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


class UserRead(BaseModel):
    id: int
    employee_id: str
    email: EmailStr
    full_name: str
    role: str
    department: str
    is_active: bool

    class Config:
        from_attributes = True
