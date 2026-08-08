import time
from typing import Dict, Any
from sqlalchemy.orm import Session

from backend.agents.base_agent import BaseAgent
from backend.agents.agent_context import AgentContext
from backend.orchestrator.response_models import IntakeOutput


class IntelligentCaseIntakeAgent(BaseAgent):
    """Agent 1: Intelligent Case Intake Agent for intent, priority, classification, and entity extraction."""

    def __init__(self):
        super().__init__(name="IntelligentCaseIntakeAgent", step_number=1)

    def _generate_fallback(self, user_prompt: str) -> Dict[str, Any]:
        prompt_lower = user_prompt.lower()
        
        # Classification & Intent determination
        if "double" in prompt_lower or "twice" in prompt_lower or "two times" in prompt_lower:
            classification = "DOUBLE_CHARGE"
            intent = "DISPUTE_DOUBLE_CHARGE"
            priority = "HIGH"
        elif "unauthorized" in prompt_lower or "stolen" in prompt_lower or "fraud" in prompt_lower:
            classification = "UNAUTHORIZED_TRANSACTION"
            intent = "REPORT_FRAUD"
            priority = "CRITICAL"
        elif "failed" in prompt_lower or "pending" in prompt_lower or "debited" in prompt_lower:
            classification = "FAILED_TRANSFER"
            intent = "CLAIM_FAILED_TRANSACTION_REFUND"
            priority = "MEDIUM"
        elif "fee" in prompt_lower or "charge" in prompt_lower:
            classification = "FEE_DISPUTE"
            intent = "REVERSAL_OF_SERVICE_FEE"
            priority = "LOW"
        else:
            classification = "GENERAL_COMPLAINT"
            intent = "CUSTOMER_SERVICE_QUERY"
            priority = "MEDIUM"

        return {
            "intent": intent,
            "priority": priority,
            "classification": classification,
            "extracted_entities": {
                "dispute_keywords": ["charge", "transaction", "amount"],
                "channel": "MOBILE_APP",
                "customer_claim": user_prompt
            },
            "summary": f"Case classified as {classification} with intent {intent} and {priority} priority."
        }

    def execute(self, context: AgentContext, db: Session) -> AgentContext:
        start_time = time.time()
        self.logger.info(f"[{self.name}] Initiating case intake for investigation ID: {context.investigation_id}")

        user_prompt = (
            f"Customer Complaint:\n{context.complaint_text}\n\n"
            f"Dispute Amount: {context.dispute_amount} {context.currency}\n"
            f"Customer ID: {context.customer_id}\n\n"
            "Analyze intent, priority (LOW, MEDIUM, HIGH, CRITICAL), issue classification, and extract entities."
        )

        output_dict = self.call_llm(user_prompt, IntakeOutput)
        
        # Validate output schema structure
        try:
            validated = IntakeOutput(**output_dict)
            structured_data = validated.model_dump()
        except Exception:
            structured_data = output_dict

        context.structured_investigation = structured_data
        
        execution_time_ms = (time.time() - start_time) * 1000
        self.persist_step(
            context=context,
            db=db,
            action_taken="INTAKE_CLASSIFICATION_COMPLETED",
            output_payload=structured_data,
            execution_time_ms=execution_time_ms
        )

        return context
