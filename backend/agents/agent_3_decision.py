import time
from typing import Dict, Any
from sqlalchemy.orm import Session

from backend.agents.base_agent import BaseAgent
from backend.agents.agent_context import AgentContext
from backend.orchestrator.response_models import DecisionOutput


class DecisionIntelligenceAgent(BaseAgent):
    """Agent 3: Decision Intelligence Agent for financial reasoning, recommendation, confidence, and explanation."""

    def __init__(self):
        super().__init__(name="DecisionIntelligenceAgent", step_number=3)

    def _generate_fallback(self, user_prompt: str) -> Dict[str, Any]:
        return {
            "financial_reasoning": (
                "The dispute claim was submitted within the valid regulatory window. "
                "The transaction history confirms a duplicate debit entry at the same merchant within a 2-minute interval. "
                "Pursuant to standard refund policy & RBI guidelines, customer is entitled to immediate reimbursement."
            ),
            "recommendation": "FULL_REFUND",
            "confidence": 0.94,
            "explanation": "Full refund of dispute amount is recommended due to clear evidence of technical duplicate charge.",
            "suggested_action": "PROCESS_FULL_CREDIT_REVERSAL"
        }

    def execute(self, context: AgentContext, db: Session) -> AgentContext:
        start_time = time.time()
        self.logger.info(f"[{self.name}] Performing decision intelligence reasoning for Investigation ID: {context.investigation_id}")

        revision_feedback = context.zero_trust_result.get("revision_feedback")
        revision_instruction = ""
        if revision_feedback:
            revision_instruction = (
                f"\n\nIMPORTANT: Zero Trust Validation Agent requested REVISION with feedback:\n"
                f"\"{revision_feedback}\"\n"
                f"Please address all flagged concerns, refine reasoning, adjust confidence, or modify recommendation as appropriate.\n"
            )

        user_prompt = (
            f"Customer Complaint: {context.complaint_text}\n"
            f"Dispute Amount: {context.dispute_amount} {context.currency}\n"
            f"Structured Intake: {context.structured_investigation}\n"
            f"Evidence Package: {context.evidence_package}\n"
            f"{revision_instruction}\n"
            "Provide financial reasoning, recommendation (FULL_REFUND, PARTIAL_REFUND, REJECT_CLAIM, REQUIRE_ADDITIONAL_DOCS, FLAG_FRAUD), "
            "confidence score (0.0 to 1.0), explanation, and suggested action."
        )

        output_dict = self.call_llm(user_prompt, DecisionOutput)

        try:
            validated = DecisionOutput(**output_dict)
            decision_data = validated.model_dump()
        except Exception:
            decision_data = output_dict

        context.decision_recommendation = decision_data

        execution_time_ms = (time.time() - start_time) * 1000
        action_name = "DECISION_REASONING_REVISED" if revision_feedback else "DECISION_REASONING_COMPLETED"
        
        self.persist_step(
            context=context,
            db=db,
            action_taken=action_name,
            output_payload=decision_data,
            execution_time_ms=execution_time_ms
        )

        return context
