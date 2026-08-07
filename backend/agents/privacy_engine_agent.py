import json
import re
import time
from sqlalchemy.orm import Session
from backend.agents.base import BaseAgent
from backend.schemas.agent import AgentContext, AgentExecutionResult
from backend.logging import logger


class ZeroKnowledgePrivacyEngine(BaseAgent):
    """6. Zero Knowledge Privacy Engine: Redacts PII / PCI before downstream processing."""

    def __init__(self):
        super().__init__(name="ZeroKnowledgePrivacyEngine", step_number=2)

    def _generate_fallback_response(self, user_prompt: str) -> str:
        redacted = user_prompt
        pii_found = False
        types = []

        # Card numbers (16 digits)
        if re.search(r'\b(?:\d[ -]*?){13,16}\b', redacted):
            redacted = re.sub(r'\b(?:\d[ -]*?){13,16}\b', '[REDACTED_CARD_NUMBER]', redacted)
            pii_found = True
            types.append("CARD_NUMBER")

        # Phone numbers
        if re.search(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', redacted):
            redacted = re.sub(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', '[REDACTED_PHONE]', redacted)
            pii_found = True
            types.append("PHONE_NUMBER")

        # Email
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', redacted):
            redacted = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', redacted)
            pii_found = True
            types.append("EMAIL")

        return json.dumps({
            "redacted_text": redacted,
            "pii_detected": pii_found,
            "redacted_types": types
        })

    def execute(self, context: AgentContext, db: Session) -> AgentExecutionResult:
        start_time = time.time()
        logger.info(f"[{self.name}] Step {self.step_number}: Redacting PII & PCI data...")

        text_to_redact = context.complaint_text
        prompt = f"Sanitize and redact sensitive info from text:\n\n\"{text_to_redact}\""
        raw_output = self.call_llm(prompt)

        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed = json.loads(self._generate_fallback_response(text_to_redact))

        # Update Context
        context.redacted_text = parsed.get("redacted_text", text_to_redact)
        context.metadata["pii_redact_summary"] = parsed

        elapsed_ms = (time.time() - start_time) * 1000
        hash_sig = self.compute_hash(text_to_redact, raw_output)

        return AgentExecutionResult(
            agent_name=self.name,
            step_number=self.step_number,
            success=True,
            action_taken="Executed Zero Knowledge PII/PCI redaction",
            output_data=parsed,
            execution_time_ms=round(elapsed_ms, 2),
            hash_signature=hash_sig
        )
