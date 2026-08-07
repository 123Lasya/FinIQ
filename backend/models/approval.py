from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.database import Base, TimestampMixin
from backend.models.enums import ApprovalStatus
from backend.utils.uuid_utils import generate_uuid


class Approval(Base, TimestampMixin):
    __tablename__ = "approvals"

    approval_id = Column(String(36), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(36), ForeignKey("investigations.investigation_id"), nullable=False, index=True)
    reviewed_by = Column(String(36), ForeignKey("employees.employee_id"), nullable=False)
    status = Column(SQLEnum(ApprovalStatus), nullable=False, default=ApprovalStatus.PENDING)
    reason = Column(Text, nullable=False)
    reviewed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    investigation = relationship("Investigation", back_populates="approvals")
    reviewer = relationship("Employee", back_populates="approvals")
