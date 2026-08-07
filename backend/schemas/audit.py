from datetime import datetime
from pydantic import BaseModel
from backend.models.enums import ComplianceStatus


class AuditLogResponse(BaseModel):
    audit_id: str
    investigation_id: str
    audit_hash: str
    decision_type: str
    compliance_status: ComplianceStatus
    remarks: str
    created_at: datetime

    class Config:
        from_attributes = True
