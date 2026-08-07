from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from backend.models.enums import InvestigationIssueType, InvestigationPriority, InvestigationStatus


class InvestigationCreate(BaseModel):
    customer_id: str
    title: str
    description: str
    issue_type: InvestigationIssueType = InvestigationIssueType.DOUBLE_CHARGE
    priority: InvestigationPriority = InvestigationPriority.MEDIUM


class InvestigationResponse(BaseModel):
    investigation_id: str
    token_id: str
    customer_id: str
    title: str
    description: str
    issue_type: InvestigationIssueType
    priority: InvestigationPriority
    status: InvestigationStatus
    current_agent: Optional[str] = None
    decision_type: Optional[str] = None
    final_decision: Optional[str] = None
    created_by: str
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
