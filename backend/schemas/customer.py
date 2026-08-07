from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from backend.models.enums import CustomerRiskLevel


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    account_number: str
    risk_level: CustomerRiskLevel = CustomerRiskLevel.LOW


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    customer_id: str
    customer_since: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
