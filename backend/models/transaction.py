from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.database import Base, TimestampMixin
from backend.models.enums import TransactionType, TransactionStatus


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    transaction_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(36), ForeignKey("customers.customer_id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False, default=TransactionType.DEBIT)
    status = Column(SQLEnum(TransactionStatus), nullable=False, default=TransactionStatus.SUCCESS)
    merchant = Column(String(120), nullable=False)
    payment_method = Column(String(50), nullable=False, default="CREDIT_CARD")
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="transactions")
