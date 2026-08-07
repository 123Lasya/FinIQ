from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from backend.models.enums import ApprovalStatus


class ApprovalCreate(BaseModel):
    investigation_id: str
    status: ApprovalStatus
    reason: str


class ApprovalResponse(BaseModel):
    approval_id: str
    investigation_id: str
    reviewed_by: str
    status: ApprovalStatus
    reason: str
    reviewed_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
