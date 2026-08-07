from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.database import Base, TimestampMixin
from backend.models.enums import InvestigationIssueType, InvestigationPriority, InvestigationStatus
from backend.utils.uuid_utils import generate_uuid, generate_token_id


class Investigation(Base, TimestampMixin):
    __tablename__ = "investigations"

    investigation_id = Column(String(36), primary_key=True, default=generate_uuid)
    token_id = Column(String(50), unique=True, index=True, nullable=False, default=generate_token_id)
    customer_id = Column(String(36), ForeignKey("customers.customer_id"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    issue_type = Column(SQLEnum(InvestigationIssueType), nullable=False, default=InvestigationIssueType.DOUBLE_CHARGE)
    priority = Column(SQLEnum(InvestigationPriority), nullable=False, default=InvestigationPriority.MEDIUM)
    status = Column(SQLEnum(InvestigationStatus), nullable=False, default=InvestigationStatus.PENDING)
    
    current_agent = Column(String(80), nullable=True)
    decision_type = Column(String(50), nullable=True)
    final_decision = Column(String(80), nullable=True)
    
    created_by = Column(String(36), ForeignKey("employees.employee_id"), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="investigations")
    creator = relationship("Employee", back_populates="created_investigations", foreign_keys=[created_by])
    execution_logs = relationship("AgentExecutionLog", back_populates="investigation", cascade="all, delete-orphan")
    artifacts = relationship("AgentArtifact", back_populates="investigation", cascade="all, delete-orphan")
    approvals = relationship("Approval", back_populates="investigation", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="investigation", cascade="all, delete-orphan")
