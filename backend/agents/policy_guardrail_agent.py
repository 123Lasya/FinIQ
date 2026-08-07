import json
import time
from sqlalchemy.orm import Session
from backend.agents.base import BaseAgent
from backend.schemas.agent import AgentContext, AgentExecutionResult
from backend.config import settings
from backend.logging import logger


class PolicyGuardrailAgent(BaseAgent):
    """7. Policy Guardrail Agent: Enforces compliance bounds and auto-approval threshold caps."""

    def __init__(self):
        super().__init__(name="PolicyGuardrailAgent", step_number=7)
        self.threshold = settings.AUTO_APPROVAL_THRESHOLD_INR

    def _generate_fallback_response(self, user_prompt: str) -> str:
        # Determine based on prompt text
        is_above = "exceeds" in user_prompt or "50000" in user_prompt
        return json.dumps({
            "guardrail_passed": True,
            "human_approval_required": is_above,
            "auto_execution_allowed": not is_above,
            "violations": ["Refund amount exceeds auto-approval threshold of ₹25,000. Human sign-off required."] if is_above else []
        })

    def execute(self, context: AgentContext, db: Session) -> AgentExecutionResult:
        start_time = time.time()
        logger.info(f"[{self.name}] Step {self.step_number}: Evaluating compliance policy guardrails (Cap: ₹{self.threshold})...")

        violations = []
        requires_human = False

        # Rule 1: Threshold Cap Check
        if context.dispute_amount > self.threshold:
            violations.append(
                f"Dispute amount (₹{context.dispute_amount:,.2f}) exceeds autonomous approval limit of ₹{self.threshold:,.2f}. Compliance policy mandates Human Officer sign-off."
            )
            requires_human = True

        # Rule 2: Low confidence check
        if context.confidence_score < 0.85:
            violations.append(
                f"Model confidence score ({context.confidence_score:.2f}) is below confidence threshold (0.85). Requires human review."
            )
            requires_human = True

        # Rule 3: Zero trust check
        if not context.zero_trust_validated:
            violations.append("Zero Trust validation did not pass cleanly. Mandatory human review triggered.")
            requires_human = True

        context.policy_guardrail_passed = (len(violations) == 0)
        context.policy_violations = violations
        context.human_approval_required = requires_human
        context.auto_executed = not requires_human

        prompt = f"Evaluate policy guardrails for amount ₹{context.dispute_amount}, threshold ₹{self.threshold}, confidence {context.confidence_score}. Violations: {json.dumps(violations)}"
        raw_output = self.call_llm(prompt)

        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed = json.loads(self._generate_fallback_response(prompt))

        elapsed_ms = (time.time() - start_time) * 1000
        hash_sig = self.compute_hash(prompt, raw_output)

        return AgentExecutionResult(
            agent_name=self.name,
            step_number=self.step_number,
            success=True,
            action_taken=f"Evaluated policy guardrails (Human Approval Required: {requires_human})",
            output_data={
                "guardrail_passed": context.policy_guardrail_passed,
                "human_approval_required": requires_human,
                "auto_execution_allowed": not requires_human,
                "violations": violations,
                "threshold_inr": self.threshold
            },
            execution_time_ms=round(elapsed_ms, 2),
            hash_signature=hash_sig
        )
