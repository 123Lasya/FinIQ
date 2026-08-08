import time
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.logging import logger
from backend.agents.agent_context import AgentContext
from backend.agents.agent_1_intake import IntelligentCaseIntakeAgent
from backend.agents.agent_2_context import EnterpriseContextRetrievalAgent
from backend.agents.agent_3_decision import DecisionIntelligenceAgent
from backend.agents.agent_4_zero_trust import ZeroTrustDecisionValidationAgent
from backend.agents.agent_5_shadow import PreFlightShadowSimulationAgent
from backend.agents.agent_6_privacy import ZeroKnowledgePrivacyEngine
from backend.agents.agent_7_guardrail import PolicyGuardrailAgent
from backend.agents.agent_8_execution import ExecutionAgent
from backend.agents.agent_9_audit import AuditAgent
from backend.models import Investigation
from backend.models.enums import InvestigationStatus


class WorkflowOrchestrator:
    """Enterprise 9-Agent AI Pipeline Controller with live database streaming for 1s polling and Zero-Trust single revision loop."""

    def __init__(self):
        self.agent_1_intake = IntelligentCaseIntakeAgent()
        self.agent_2_context = EnterpriseContextRetrievalAgent()
        self.agent_3_decision = DecisionIntelligenceAgent()
        self.agent_4_zero_trust = ZeroTrustDecisionValidationAgent()
        self.agent_5_shadow = PreFlightShadowSimulationAgent()
        self.agent_6_privacy = ZeroKnowledgePrivacyEngine()
        self.agent_7_guardrail = PolicyGuardrailAgent()
        self.agent_8_execution = ExecutionAgent()
        self.agent_9_audit = AuditAgent()

    def run_investigation_pipeline(self, investigation_id_or_token: str, db: Session) -> AgentContext:
        """Executes full 9-agent investigation workflow, updating MySQL DB after every completed agent."""
        logger.info(f"[WorkflowOrchestrator] Starting 9-agent AI pipeline for investigation: {investigation_id_or_token}")

        # Fetch investigation by investigation_id OR token_id
        inv = db.query(Investigation).filter(
            (Investigation.investigation_id == investigation_id_or_token) |
            (Investigation.token_id == investigation_id_or_token)
        ).first()

        if not inv:
            raise ValueError(f"Investigation record {investigation_id_or_token} not found in database.")

        inv.status = InvestigationStatus.IN_PROGRESS
        inv.current_agent = "IntelligentCaseIntakeAgent"
        db.commit()

        # Initialize unified Agent Context
        context = AgentContext(
            investigation_id=inv.investigation_id,
            token_id=inv.token_id,
            customer_id=inv.customer_id,
            customer_complaint=inv.description,
            dispute_amount=getattr(inv, "dispute_amount", 0.0) or 0.0,
            currency="INR"
        )

        try:
            # Step 1: Intelligent Case Intake Agent
            context = self.agent_1_intake.execute(context, db)

            # Step 2: Enterprise Context Retrieval Agent
            context = self.agent_2_context.execute(context, db)

            # Step 3: Decision Intelligence Agent
            context = self.agent_3_decision.execute(context, db)

            # Step 4: Zero Trust Decision Validation Agent
            context = self.agent_4_zero_trust.execute(context, db)

            # Check if Zero Trust requested REVISION and no revision has been performed yet
            zero_trust_status = context.zero_trust_result.get("status")
            if zero_trust_status == "REVISE" and context.revision_count < 1:
                logger.info(f"[WorkflowOrchestrator] Zero Trust requested REVISION. Returning ONLY ONCE to Agent 3 with feedback.")
                context.revision_count += 1

                # Re-run Agent 3 with Zero Trust feedback
                context = self.agent_3_decision.execute(context, db)

                # Skip second Zero Trust validation and enforce protocol
                context.skip_zero_trust = True
                logger.info(f"[WorkflowOrchestrator] Post-revision: skipping second Zero Trust validation as per single revision limit.")

            # Step 5: Pre Flight Shadow Simulation Agent
            context = self.agent_5_shadow.execute(context, db)

            # Step 6: Privacy Engine (PII Tokenizer)
            context = self.agent_6_privacy.execute(context, db)

            # Step 7: Policy Guardrail Agent
            context = self.agent_7_guardrail.execute(context, db)

            # Step 8: Execution Agent
            context = self.agent_8_execution.execute(context, db)

            # Step 9: Cryptographic Audit Agent
            context = self.agent_9_audit.execute(context, db)

            logger.info(f"[WorkflowOrchestrator] Successfully completed all 9 agents for investigation {inv.investigation_id}. Final status: {context.status}")

        except Exception as e:
            logger.error(f"[WorkflowOrchestrator] Pipeline execution failure: {e}", exc_info=True)
            inv.status = InvestigationStatus.REQUIRES_HUMAN_APPROVAL
            inv.current_agent = "ERROR_HALTED"
            db.commit()
            raise e

        return context
