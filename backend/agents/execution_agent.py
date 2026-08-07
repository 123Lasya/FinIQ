import json
import time
import uuid
from sqlalchemy.orm import Session
from backend.agents.base import BaseAgent
from backend.schemas.agent import AgentContext, AgentExecutionResult
from backend.logging import logger


class ExecutionAgent(BaseAgent):
    """8. Execution Agent: Commits financial disbursement or flags case for human approval queue."""

    def __init__(self):
        super().__init__(name="ExecutionAgent", step_number=8)

    def _generate_fallback_response(self, user_prompt: str) -> str:
        is_held = "held" in user_prompt.lower() or "human" in user_prompt.lower()
        return json.dumps({
            "execution_status": "HELD_FOR_APPROVAL" if is_held else "EXECUTED",
            "disbursement_reference": f"DISB-{uuid.uuid4().hex[:8].upper()}",
            "notification_payload": "Disbursement queued awaiting Human Operations Executive sign-off." if is_held else "Disbursement executed automatically."
        })

    def execute(self, context: AgentContext, db: Session) -> AgentExecutionResult:
        start_time = time.time()
        logger.info(f"[{self.name}] Step {self.step_number}: Executing disbursement decision pipeline...")

        if context.human_approval_required and not context.auto_executed:
            exec_status = "HELD_FOR_APPROVAL"
            disb_ref = f"HOLD-{uuid.uuid4().hex[:8].upper()}"
            msg = f"Dispute amount ₹{context.dispute_amount:,.2f} exceeds auto-approval threshold. Token placed in Incoming Queue for Human Approval."
        else:
            exec_status = "EXECUTED"
            disb_ref = f"DISB-REFUND-{uuid.uuid4().hex[:8].upper()}"
            msg = f"Disbursement of {context.currency} {context.dispute_amount:,.2f} successfully executed."

        result_payload = {
            "execution_status": exec_status,
            "disbursement_reference": disb_ref,
            "notification_payload": msg,
            "auto_executed": context.auto_executed
        }
        context.execution_result = result_payload

        prompt = f"Execution details: {json.dumps(result_payload)}"
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
            action_taken=f"Execution pipeline finished with status: {exec_status}",
            output_data=parsed,
            execution_time_ms=round(elapsed_ms, 2),
            hash_signature=hash_sig
        )
