from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.investigation import Investigation
from backend.schemas.investigation import InvestigationCreate
from backend.models.enums import InvestigationStatus
from backend.utils.uuid_utils import generate_token_id
from backend.utils.exceptions import ResourceNotFoundException


class InvestigationService:
    """Service layer for Investigation Token operations."""

    @staticmethod
    def get_by_id(db: Session, investigation_id: str) -> Investigation:
        inv = db.query(Investigation).filter(Investigation.investigation_id == investigation_id).first()
        if not inv:
            raise ResourceNotFoundException("Investigation", investigation_id)
        return inv

    @staticmethod
    def get_by_token_id(db: Session, token_id: str) -> Investigation:
        inv = db.query(Investigation).filter(Investigation.token_id == token_id).first()
        if not inv:
            raise ResourceNotFoundException("Investigation Token", token_id)
        return inv

    @staticmethod
    def create_investigation(db: Session, payload: InvestigationCreate, created_by_id: str) -> Investigation:
        token_id = generate_token_id()
        inv = Investigation(
            token_id=token_id,
            customer_id=payload.customer_id,
            title=payload.title,
            description=payload.description,
            issue_type=payload.issue_type,
            priority=payload.priority,
            status=InvestigationStatus.PENDING,
            created_by=created_by_id
        )
        db.add(inv)
        db.commit()
        db.refresh(inv)
        return inv

    @staticmethod
    def list_investigations(db: Session, status: Optional[InvestigationStatus] = None) -> List[Investigation]:
        query = db.query(Investigation)
        if status:
            query = query.filter(Investigation.status == status)
        return query.order_by(Investigation.created_at.desc()).all()
