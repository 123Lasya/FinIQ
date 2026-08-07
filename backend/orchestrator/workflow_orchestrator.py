import json
import time
from sqlalchemy.orm import Session

from backend.agents import (
    IntelligentCaseIntakeAgent,
    ZeroKnowledgePrivacyEngine,
    EnterpriseContextRetrievalAgent,
    DecisionIntelligenceAgent,
    ZeroTrustDecisionValidationAgent,
    PreFlightShadowSimulationAgent,
    PolicyGuardrailAgent,
    ExecutionAgent,
    AuditAgent
)
from backend.models import Investigation, AuditLog
from backend.schemas.agent import AgentContext
from backend.logging import logger


class WorkflowOrchestrator:
    """Enterprise Multi-Agent Pipeline Controller for FinPilot AI."""

    def __init__(self):
        self.intake_agent = IntelligentCaseIntakeAgent()
        self.privacy_agent = ZeroKnowledgePrivacyEngine()
        self.context_agent = EnterpriseContextRetrievalAgent()
        self.decision_agent = DecisionIntelligenceAgent()
        self.zero_trust_agent = ZeroTrustDecisionValidationAgent()
        self.shadow_agent = PreFlightShadowSimulationAgent()
        self.guardrail_agent = PolicyGuardrailAgent()
        self.execution_agent = ExecutionAgent()
        self.audit_agent = AuditAgent()

    def run_investigation_pipeline(self, token_id: str, db: Session) -> AgentContext:
        """Executes the full 9-agent investigation workflow for an Investigation Token."""
        logger.info(f"[WorkflowOrchestrator] Starting multi-agent investigation pipeline for Token: {token_id}")

        inv = db.query(Investigation).filter(Investigation.token_id == token_id).first()
        if not inv:
            raise ValueError(f"Investigation token {token_id} not found in database.")

        inv.status = "IN_PROGRESS"
        db.commit()

        # Initialize Agent Context
        context = AgentContext(
            token_id=inv.token_id,
            customer_id=inv.customer_id,
            complaint_text=inv.complaint_text,
            dispute_amount=inv.dispute_amount,
            currency=inv.currency
        )

        pipeline_agents = [
            self.intake_agent,
            self.privacy_agent,
            self.context_agent,
            self.decision_agent,
            self.zero_trust_agent,
            self.shadow_agent,
            self.guardrail_agent,
            self.execution_agent,
            self.audit_agent
        ]

        for agent in pipeline_agents:
            logger.info(f"[Orchestrator] Running Agent Step {agent.step_number}: {agent.name}")
            result = agent.execute(context, db)

            # Persist Audit Log step
            audit_entry = AuditLog(
                investigation_token_id=context.token_id,
                agent_name=agent.name,
                step_number=agent.step_number,
                action=result.action_taken,
                input_payload=json.dumps({"complaint_text": context.complaint_text, "dispute_amount": context.dispute_amount}),
                output_payload=json.dumps(result.output_data),
                execution_time_ms=result.execution_time_ms,
                hash_signature=result.hash_signature
            )
            db.add(audit_entry)
            db.commit()

        # Update Investigation Database Record with finalized state
        inv.dispute_amount = context.dispute_amount
        inv.redacted_text = context.redacted_text
        inv.final_decision = context.recommended_decision
        inv.confidence_score = context.confidence_score
        inv.decision_reasoning = context.reasoning
        inv.shadow_simulation_result = json.dumps(context.shadow_simulation_details)
        inv.zero_trust_status = "PASSED" if context.zero_trust_validated else "FAILED"
        inv.pii_redacted = bool(context.redacted_text)
        inv.human_approval_required = context.human_approval_required
        inv.auto_executed = context.auto_executed

        if context.human_approval_required:
            inv.status = "REQUIRES_HUMAN_APPROVAL"
        else:
            inv.status = "AUTO_EXECUTED"

        db.commit()
        db.refresh(inv)

        logger.info(f"[WorkflowOrchestrator] Completed investigation pipeline for {token_id}. Final Status: {inv.status}")
        return context
