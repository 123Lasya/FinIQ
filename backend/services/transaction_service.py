from typing import List
from sqlalchemy.orm import Session
from backend.models.transaction import Transaction
from backend.schemas.transaction import TransactionCreate
from backend.utils.exceptions import ResourceNotFoundException


class TransactionService:
    """Service layer for financial ledger Transaction operations."""

    @staticmethod
    def get_by_id(db: Session, transaction_id: str) -> Transaction:
        txn = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
        if not txn:
            raise ResourceNotFoundException("Transaction", transaction_id)
        return txn

    @staticmethod
    def get_by_customer(db: Session, customer_id: str) -> List[Transaction]:
        return db.query(Transaction).filter(Transaction.customer_id == customer_id).all()

    @staticmethod
    def create_transaction(db: Session, payload: TransactionCreate) -> Transaction:
        txn = Transaction(
            transaction_id=payload.transaction_id,
            customer_id=payload.customer_id,
            amount=payload.amount,
            transaction_type=payload.transaction_type,
            status=payload.status,
            merchant=payload.merchant,
            payment_method=payload.payment_method
        )
        db.add(txn)
        db.commit()
        db.refresh(txn)
        return txn

    @staticmethod
    def list_transactions(db: Session) -> List[Transaction]:
        return db.query(Transaction).all()
