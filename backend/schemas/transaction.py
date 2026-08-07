from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from backend.models.enums import TransactionType, TransactionStatus


class TransactionBase(BaseModel):
    transaction_id: str
    customer_id: str
    amount: float
    transaction_type: TransactionType = TransactionType.DEBIT
    status: TransactionStatus = TransactionStatus.SUCCESS
    merchant: str
    payment_method: str = "CREDIT_CARD"


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
