from typing import Optional
from sqlalchemy.orm import Session
from backend.repositories.base import BaseRepository
from backend.models.customer import Customer


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self):
        super().__init__(Customer)

    def get_by_customer_id(self, db: Session, customer_id: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.customer_id == customer_id).first()

    def get_by_account_number(self, db: Session, account_number: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.account_number == account_number).first()
