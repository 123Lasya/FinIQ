from sqlalchemy import Column, String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.database import Base, TimestampMixin
from backend.models.enums import ComplianceStatus
from backend.utils.uuid_utils import generate_uuid


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    audit_id = Column(String(36), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(36), ForeignKey("investigations.investigation_id"), nullable=False, index=True)
    audit_hash = Column(String(128), nullable=False)
    decision_type = Column(String(50), nullable=False)
    compliance_status = Column(SQLEnum(ComplianceStatus), nullable=False, default=ComplianceStatus.PASSED)
    remarks = Column(Text, nullable=False)

    # Relationships
    investigation = relationship("Investigation", back_populates="audit_logs")
