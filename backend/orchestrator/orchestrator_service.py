import threading
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.logging import logger
from backend.orchestrator.workflow import WorkflowOrchestrator
from backend.agents.agent_context import AgentContext
from backend.models import Investigation
from backend.models.enums import InvestigationStatus


class OrchestratorService:
    """Enterprise Orchestrator Service for start/trigger requests from POST /api/investigations/start."""

    def __init__(self):
        self.orchestrator = WorkflowOrchestrator()

    def start_investigation(
        self,
        investigation_id_or_token: str,
        db: Session,
        run_in_background: bool = False
    ) -> Dict[str, Any]:
        """Entry point called by POST /api/investigations/start.
        Triggers full 9-agent pipeline execution.
        """
        logger.info(f"[OrchestratorService] Received start trigger for investigation: {investigation_id_or_token}")

        inv = db.query(Investigation).filter(
            (Investigation.investigation_id == investigation_id_or_token) |
            (Investigation.token_id == investigation_id_or_token)
        ).first()

        if not inv:
            raise ValueError(f"Investigation {investigation_id_or_token} not found.")

        if run_in_background:
            # Run asynchronously in background thread so caller returns immediately and polling updates DB
            def worker():
                from backend.database import SessionLocal
                bg_db = SessionLocal()
                try:
                    self.orchestrator.run_investigation_pipeline(inv.investigation_id, bg_db)
                except Exception as err:
                    logger.error(f"[OrchestratorService] Background pipeline error: {err}")
                finally:
                    bg_db.close()

            t = threading.Thread(target=worker, daemon=True)
            t.start()

            return {
                "investigation_id": inv.investigation_id,
                "token_id": inv.token_id,
                "status": "IN_PROGRESS",
                "message": "AI Orchestration pipeline started in background. Poll GET /api/investigations/{id} for live execution progress."
            }

        # Synchronous execution
        context = self.orchestrator.run_investigation_pipeline(inv.investigation_id, db)

        return {
            "investigation_id": context.investigation_id,
            "token_id": context.token_id,
            "status": context.status,
            "current_agent": context.current_agent,
            "recommendation": context.decision_recommendation.get("recommendation"),
            "confidence": context.confidence_score,
            "zero_trust_status": context.zero_trust_result.get("status"),
            "execution_type": context.execution_result.get("execution_type"),
            "audit_hash": context.audit_trail.get("audit_hash")
        }


# Singleton service instance
orchestrator_service = OrchestratorService()
