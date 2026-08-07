from datetime import datetime
from sqlalchemy import Column, String, Float, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.database import Base, TimestampMixin
from backend.models.enums import AgentExecutionStatus
from backend.utils.uuid_utils import generate_uuid


class AgentExecutionLog(Base, TimestampMixin):
    __tablename__ = "agent_execution_logs"

    execution_id = Column(String(36), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(36), ForeignKey("investigations.investigation_id"), nullable=False, index=True)
    agent_name = Column(String(80), nullable=False)
    status = Column(SQLEnum(AgentExecutionStatus), nullable=False, default=AgentExecutionStatus.RUNNING)
    execution_time = Column(Float, default=0.0, nullable=False)
    confidence = Column(Float, default=0.0, nullable=False)
    model_used = Column(String(80), nullable=False, default="llama-3.3-70b-versatile")
    
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    investigation = relationship("Investigation", back_populates="execution_logs")


class AgentArtifact(Base, TimestampMixin):
    __tablename__ = "agent_artifacts"

    artifact_id = Column(String(36), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(36), ForeignKey("investigations.investigation_id"), nullable=False, index=True)
    agent_name = Column(String(80), nullable=False)
    artifact_type = Column(String(50), nullable=False)
    artifact_json = Column(Text, nullable=False)

    # Relationships
    investigation = relationship("Investigation", back_populates="artifacts")
