from typing import List
from sqlalchemy.orm import Session
from backend.repositories.base import BaseRepository
from backend.models.transaction import Transaction


class TransactionRepository(BaseRepository[Transaction]):
    def __init__(self):
        super().__init__(Transaction)

    def get_by_customer_id(self, db: Session, customer_id: str, limit: int = 20) -> List[Transaction]:
        return db.query(Transaction).filter(
            Transaction.customer_id == customer_id
        ).order_by(Transaction.timestamp.desc()).limit(limit).all()
