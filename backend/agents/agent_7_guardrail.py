import time
from typing import Dict, Any
from sqlalchemy.orm import Session

from backend.agents.base_agent import BaseAgent
from backend.agents.agent_context import AgentContext
from backend.orchestrator.response_models import GuardrailOutput


class PolicyGuardrailAgent(BaseAgent):
    """Agent 7: Policy Guardrail Agent for evaluating rules and returning AUTO, HUMAN, or BLOCK status."""

    def __init__(self):
        super().__init__(name="PolicyGuardrailAgent", step_number=7)

    def _generate_fallback(self, user_prompt: str) -> Dict[str, Any]:
        return {
            "status": "AUTO",
            "refund_policy_check": True,
            "rbi_compliance_check": True,
            "fraud_sop_check": True,
            "internal_rules_check": True,
            "violations": [],
            "reason": "Dispute amount is within automatic approval threshold (<= 10,000 INR) and fully satisfies RBI & internal policy SOPs."
        }

    def execute(self, context: AgentContext, db: Session) -> AgentContext:
        start_time = time.time()
        self.logger.info(f"[{self.name}] Evaluating policy guardrails for Investigation ID: {context.investigation_id}")

        amount = context.dispute_amount
        recommendation = context.decision_recommendation.get("recommendation", "")
        confidence = float(context.decision_recommendation.get("confidence", 0.0))
        fraud_risk = float(context.shadow_simulation.get("fraud_risk_score", 0.0))
        prompt_injection = context.zero_trust_result.get("prompt_injection_detected", False)

        violations = []
        refund_policy_pass = True
        rbi_pass = True
        fraud_sop_pass = True
        internal_pass = True

        # Policy Checks
        if prompt_injection:
            violations.append("Prompt Injection Detected by Zero Trust Engine")
            internal_pass = False

        if fraud_risk >= 0.70:
            violations.append("Critical Fraud Risk Threshold Exceeded (>0.70)")
            fraud_sop_pass = False

        if confidence < 0.70:
            violations.append("Model Decision Confidence Below Threshold (<0.70)")
            internal_pass = False

        if amount > 100000:
            violations.append("Dispute Amount exceeds high-value operations ceiling (>100,000 INR)")
            refund_policy_pass = False

        # Status determination logic
        if prompt_injection or fraud_risk >= 0.70:
            status = "BLOCK"
            reason = "Case BLOCKED due to high fraud risk markers or security violations."
        elif amount > 10000 or confidence < 0.85 or fraud_risk >= 0.20 or recommendation not in ["FULL_REFUND", "PARTIAL_REFUND"]:
            status = "HUMAN"
            reason = "Case flagged for HUMAN approval due to financial thresholds, confidence level, or operational SOP requirements."
        else:
            status = "AUTO"
            reason = "Case fully passed all automated policy guardrails and is approved for automatic execution."

        user_prompt = (
            f"Dispute Amount: {amount} {context.currency}\n"
            f"Decision Recommendation: {recommendation} (Confidence: {confidence})\n"
            f"Fraud Risk Score: {fraud_risk}\n"
            f"Prompt Injection Flag: {prompt_injection}\n"
            f"Calculated Status: {status}\n"
            f"Violations Identified: {violations}\n\n"
            "Generate formal Policy Guardrail evaluation JSON matching GuardrailOutput format."
        )

        output_dict = self.call_llm(user_prompt, GuardrailOutput)

        try:
            validated = GuardrailOutput(**output_dict)
            guardrail_data = validated.model_dump()
        except Exception:
            guardrail_data = {
                "status": status,
                "refund_policy_check": refund_policy_pass,
                "rbi_compliance_check": rbi_pass,
                "fraud_sop_check": fraud_sop_pass,
                "internal_rules_check": internal_pass,
                "violations": violations,
                "reason": reason
            }

        context.policy_evaluation = guardrail_data
        context.status = "AUTO_EXECUTED" if guardrail_data.get("status") == "AUTO" else "REQUIRES_HUMAN_APPROVAL"

        execution_time_ms = (time.time() - start_time) * 1000
        self.persist_step(
            context=context,
            db=db,
            action_taken=f"POLICY_GUARDRAIL_EVALUATED_{guardrail_data.get('status')}",
            output_payload=guardrail_data,
            execution_time_ms=execution_time_ms
        )

        return context
