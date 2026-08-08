from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.repositories.base import BaseRepository
from backend.models.investigation import Investigation
from backend.models.agent_log import AgentExecutionLog, AgentArtifact
from backend.models.enums import InvestigationStatus


class InvestigationRepository(BaseRepository[Investigation]):
    def __init__(self):
        super().__init__(Investigation)

    def get_by_investigation_id(self, db: Session, investigation_id: str) -> Optional[Investigation]:
        return db.query(Investigation).filter(Investigation.investigation_id == investigation_id).first()

    def get_by_token_id(self, db: Session, token_id: str) -> Optional[Investigation]:
        return db.query(Investigation).filter(Investigation.token_id == token_id).first()

    def find_by_id_or_token(self, db: Session, identifier: str) -> Optional[Investigation]:
        return db.query(Investigation).filter(
            (Investigation.investigation_id == identifier) | (Investigation.token_id == identifier)
        ).first()

    def get_queue(self, db: Session, status: Optional[str] = None) -> List[Investigation]:
        query = db.query(Investigation)
        if status:
            query = query.filter(Investigation.status == status)
        return query.order_by(desc(Investigation.created_at)).all()

    def get_execution_logs(self, db: Session, investigation_id: str) -> List[AgentExecutionLog]:
        return db.query(AgentExecutionLog).filter(
            AgentExecutionLog.investigation_id == investigation_id
        ).order_by(AgentExecutionLog.started_at.asc()).all()

    def get_artifacts(self, db: Session, investigation_id: str) -> List[AgentArtifact]:
        return db.query(AgentArtifact).filter(
            AgentArtifact.investigation_id == investigation_id
        ).all()
