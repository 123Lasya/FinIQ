from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class PolicySchema(BaseModel):
    id: Optional[int] = None
    policy_code: str
    title: str
    description: str
    max_refund_limit: float
    requires_compliance_review: bool
    is_active: bool = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PolicyCheckResult(BaseModel):
    passed: bool
    violations: List[str]
    max_allowed_refund: float
    requires_human_signoff: bool
