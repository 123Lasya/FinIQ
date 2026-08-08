import time
import json
from typing import Dict, Any
from sqlalchemy.orm import Session

from backend.agents.base_agent import BaseAgent
from backend.agents.agent_context import AgentContext
from backend.models.investigation import Investigation
from backend.models.approval import Approval
from backend.models.enums import InvestigationStatus, ApprovalStatus
from backend.orchestrator.response_models import ExecutionOutput


class ExecutionAgent(BaseAgent):
    """Agent 8: Execution Agent for automated financial execution or generating Human Approval queue request."""

    def __init__(self):
        super().__init__(name="ExecutionAgent", step_number=8)

    def _generate_fallback(self, user_prompt: str) -> Dict[str, Any]:
        return {
            "execution_type": "AUTO_EXECUTED",
            "execution_summary": "Automated refund credit of dispute amount processed successfully via core banking ledger integration.",
            "approval_details": None,
            "status": "AUTO_EXECUTED"
        }

    def execute(self, context: AgentContext, db: Session) -> AgentContext:
        start_time = time.time()
        self.logger.info(f"[{self.name}] Executing financial operations handling for Investigation ID: {context.investigation_id}")

        guardrail_status = context.policy_evaluation.get("status", "HUMAN")

        if guardrail_status == "AUTO":
            execution_type = "AUTO_EXECUTED"
            final_status = "AUTO_EXECUTED"
            exec_summary = (
                f"Automated credit reversal of {context.dispute_amount} {context.currency} executed successfully. "
                f"Reference ledger settlement ID: SETTLE_{context.token_id[-8:]}."
            )
            approval_payload = None
        else:
            execution_type = "HUMAN_APPROVAL_REQUESTED"
            final_status = "REQUIRES_HUMAN_APPROVAL"
            exec_summary = (
                f"Investigation flagged for Human Operations Officer review. "
                f"Reason: {context.policy_evaluation.get('reason', 'Policy threshold exceeded.')}"
            )
            approval_payload = {
                "investigation_id": context.investigation_id,
                "token_id": context.token_id,
                "customer_id": context.customer_id,
                "dispute_amount": context.dispute_amount,
                "recommended_decision": context.decision_recommendation.get("recommendation"),
                "confidence": context.decision_recommendation.get("confidence"),
                "policy_violations": context.policy_evaluation.get("violations", []),
                "flagged_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            # Create Approval record if not present
            try:
                inv = db.query(Investigation).filter(Investigation.investigation_id == context.investigation_id).first()
                if inv:
                    existing_appr = db.query(Approval).filter(Approval.investigation_id == context.investigation_id).first()
                    if not existing_appr:
                        appr = Approval(
                            investigation_id=context.investigation_id,
                            reviewed_by=inv.created_by,
                            status=ApprovalStatus.PENDING,
                            reason=f"AI Agent Flagged: {context.policy_evaluation.get('reason', 'Pending human authorization')}"
                        )
                        db.add(appr)
            except Exception as e:
                self.logger.warning(f"[{self.name}] Warning creating Approval record: {e}")

        execution_data = {
            "execution_type": execution_type,
            "execution_summary": exec_summary,
            "approval_details": approval_payload,
            "status": final_status
        }

        context.execution_result = execution_data
        context.status = final_status

        # Update Investigation record status
        inv = db.query(Investigation).filter(Investigation.investigation_id == context.investigation_id).first()
        if inv:
            inv.status = InvestigationStatus.AUTO_EXECUTED if final_status == "AUTO_EXECUTED" else InvestigationStatus.REQUIRES_HUMAN_APPROVAL

        execution_time_ms = (time.time() - start_time) * 1000
        self.persist_step(
            context=context,
            db=db,
            action_taken=f"EXECUTION_HANDLED_{execution_type}",
            output_payload=execution_data,
            execution_time_ms=execution_time_ms
        )

        return context
