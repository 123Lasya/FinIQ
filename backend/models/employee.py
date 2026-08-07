from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.database import Base, TimestampMixin
from backend.models.enums import EmployeeRole
from backend.utils.uuid_utils import generate_uuid


class Employee(Base, TimestampMixin):
    __tablename__ = "employees"

    employee_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    department = Column(String(80), nullable=False, default="Financial Operations")
    role = Column(SQLEnum(EmployeeRole), nullable=False, default=EmployeeRole.OPERATIONS_EXEC)

    # Relationships
    created_investigations = relationship("Investigation", back_populates="creator", foreign_keys="Investigation.created_by")
    approvals = relationship("Approval", back_populates="reviewer")
    uploaded_documents = relationship("KnowledgeDocument", back_populates="uploader")
