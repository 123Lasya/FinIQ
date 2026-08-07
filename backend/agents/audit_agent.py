import json
import time
import hashlib
from sqlalchemy.orm import Session
from backend.agents.base import BaseAgent
from backend.schemas.agent import AgentContext, AgentExecutionResult
from backend.logging import logger


class AuditAgent(BaseAgent):
    """9. Audit Agent: Synthesizes immutable compliance audit report & cryptographic telemetry."""

    def __init__(self):
        super().__init__(name="AuditAgent", step_number=9)

    def _generate_fallback_response(self, user_prompt: str) -> str:
        return json.dumps({
            "audit_summary": "Comprehensive 9-agent investigation trajectory synthesized.",
            "compliance_verified": True,
            "final_status": "AUDITED_AND_SEALED",
            "audit_hash": hashlib.sha256(user_prompt.encode("utf-8")).hexdigest()
        })

    def execute(self, context: AgentContext, db: Session) -> AgentExecutionResult:
        start_time = time.time()
        logger.info(f"[{self.name}] Step {self.step_number}: Generating immutable audit trail report...")

        audit_payload = {
            "token_id": context.token_id,
            "customer_id": context.customer_id,
            "dispute_amount": context.dispute_amount,
            "currency": context.currency,
            "recommended_decision": context.recommended_decision,
            "confidence_score": context.confidence_score,
            "zero_trust_validated": context.zero_trust_validated,
            "shadow_simulation_passed": context.shadow_simulation_passed,
            "policy_guardrail_passed": context.policy_guardrail_passed,
            "human_approval_required": context.human_approval_required,
            "auto_executed": context.auto_executed,
            "violations": context.policy_violations
        }

        # Generate cryptographic master hash
        master_raw = json.dumps(audit_payload, sort_keys=True)
        master_hash = hashlib.sha256(master_raw.encode("utf-8")).hexdigest()
        audit_payload["integrity_master_hash"] = master_hash

        context.audit_report = audit_payload

        prompt = f"Audit payload for case {context.token_id}: {json.dumps(audit_payload)}"
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
            action_taken=f"Generated cryptographic compliance audit report (Master Hash: {master_hash[:12]}...)",
            output_data=audit_payload,
            execution_time_ms=round(elapsed_ms, 2),
            hash_signature=hash_sig
        )
