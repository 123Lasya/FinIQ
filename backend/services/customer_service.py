from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.customer import Customer
from backend.schemas.customer import CustomerCreate
from backend.utils.exceptions import ResourceNotFoundException


class CustomerService:
    """Service layer for Customer profile operations."""

    @staticmethod
    def get_by_id(db: Session, customer_id: str) -> Customer:
        cust = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not cust:
            raise ResourceNotFoundException("Customer", customer_id)
        return cust

    @staticmethod
    def create_customer(db: Session, payload: CustomerCreate) -> Customer:
        cust = Customer(
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            account_number=payload.account_number,
            risk_level=payload.risk_level
        )
        db.add(cust)
        db.commit()
        db.refresh(cust)
        return cust

    @staticmethod
    def list_customers(db: Session) -> List[Customer]:
        return db.query(Customer).all()
