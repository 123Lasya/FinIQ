import json
import re
import time
from sqlalchemy.orm import Session
from backend.agents.base import BaseAgent
from backend.schemas.agent import AgentContext, AgentExecutionResult
from backend.logging import logger


class IntelligentCaseIntakeAgent(BaseAgent):
    """1. Intelligent Case Intake Agent: Extracts structured parameters from complaints."""

    def __init__(self):
        super().__init__(name="IntelligentCaseIntakeAgent", step_number=1)

    def _generate_fallback_response(self, user_prompt: str) -> str:
        # Extract currency amount (e.g. ₹50,000 or $50000 or 50000 INR)
        amount = 0.0
        match = re.search(r'(?:₹|\$|INR|USD)?\s*([\d,]+(?:\.\d+)?)', user_prompt)
        if match:
            try:
                amount = float(match.group(1).replace(",", ""))
            except ValueError:
                amount = 0.0

        claim_type = "DOUBLE_CHARGE" if "twice" in user_prompt.lower() or "double" in user_prompt.lower() else "GENERAL_DISPUTE"
        txn_matches = re.findall(r'TXN-?\d+', user_prompt, re.IGNORECASE)

        return json.dumps({
            "dispute_amount": amount,
            "currency": "INR" if "₹" in user_prompt or "inr" in user_prompt.lower() else "INR",
            "claim_type": claim_type,
            "extracted_transaction_ids": [t.upper() for t in txn_matches],
            "priority": "HIGH" if amount >= 25000 else "MEDIUM",
            "summary": "Parsed financial complaint intake payload."
        })

    def execute(self, context: AgentContext, db: Session) -> AgentExecutionResult:
        start_time = time.time()
        logger.info(f"[{self.name}] Step {self.step_number}: Executing case intake parsing...")

        text_to_parse = context.complaint_text
        prompt = f"Parse the following complaint text:\n\n\"{text_to_parse}\""
        raw_output = self.call_llm(prompt)

        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed = json.loads(self._generate_fallback_response(text_to_parse))

        # Update context
        context.dispute_amount = float(parsed.get("dispute_amount", 0.0))
        context.currency = parsed.get("currency", "INR")
        context.extracted_entities = parsed

        elapsed_ms = (time.time() - start_time) * 1000
        hash_sig = self.compute_hash(text_to_parse, raw_output)

        return AgentExecutionResult(
            agent_name=self.name,
            step_number=self.step_number,
            success=True,
            action_taken="Parsed case intake complaint & extracted structured entities",
            output_data=parsed,
            execution_time_ms=round(elapsed_ms, 2),
            hash_signature=hash_sig
        )
