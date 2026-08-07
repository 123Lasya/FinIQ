from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.database import Base, TimestampMixin
from backend.models.enums import CustomerRiskLevel
from backend.utils.uuid_utils import generate_uuid


class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    customer_id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone = Column(String(30), nullable=False)
    account_number = Column(String(40), unique=True, index=True, nullable=False)
    risk_level = Column(SQLEnum(CustomerRiskLevel), nullable=False, default=CustomerRiskLevel.LOW)
    customer_since = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    transactions = relationship("Transaction", back_populates="customer", cascade="all, delete-orphan")
    investigations = relationship("Investigation", back_populates="customer", cascade="all, delete-orphan")
