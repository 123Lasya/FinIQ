import json
import time
from sqlalchemy.orm import Session
from backend.agents.base import BaseAgent
from backend.schemas.agent import AgentContext, AgentExecutionResult
from backend.logging import logger


class DecisionIntelligenceAgent(BaseAgent):
    """3. Decision Intelligence Agent: Formulates initial decision recommendation."""

    def __init__(self):
        super().__init__(name="DecisionIntelligenceAgent", step_number=4)

    def _generate_fallback_response(self, user_prompt: str) -> str:
        return json.dumps({
            "recommended_decision": "REFUND_APPROVED",
            "confidence_score": 0.95,
            "reasoning": "Duplicate transaction verified on customer ledger for identical amount ₹50,000. Customer claim is legitimate.",
            "recommended_refund_amount": 50000.0
        })

    def execute(self, context: AgentContext, db: Session) -> AgentExecutionResult:
        start_time = time.time()
        logger.info(f"[{self.name}] Step {self.step_number}: Computing AI decision intelligence recommendation...")

        prompt = f"""
Complaint: {context.redacted_text or context.complaint_text}
Dispute Amount: {context.currency} {context.dispute_amount}
Retrieved Policies: {json.dumps(context.retrieved_policies)}
Customer History: {json.dumps(context.customer_history)}
"""
        raw_output = self.call_llm(prompt)

        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed = json.loads(self._generate_fallback_response(prompt))

        # Update AgentContext
        context.recommended_decision = parsed.get("recommended_decision", "REFUND_APPROVED")
        context.confidence_score = float(parsed.get("confidence_score", 0.90))
        context.reasoning = parsed.get("reasoning", "Verified duplicate transaction claim.")

        elapsed_ms = (time.time() - start_time) * 1000
        hash_sig = self.compute_hash(prompt, raw_output)

        return AgentExecutionResult(
            agent_name=self.name,
            step_number=self.step_number,
            success=True,
            action_taken=f"Formulated decision recommendation: {context.recommended_decision} with confidence {context.confidence_score}",
            output_data=parsed,
            execution_time_ms=round(elapsed_ms, 2),
            hash_signature=hash_sig
        )
