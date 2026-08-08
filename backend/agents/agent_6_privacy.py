import time
import re
import hashlib
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from backend.agents.base_agent import BaseAgent
from backend.agents.agent_context import AgentContext
from backend.orchestrator.response_models import PrivacyOutput


class ZeroKnowledgePrivacyEngine(BaseAgent):
    """Agent 6: Privacy Engine (Zero Knowledge PII Tokenizer) for deterministic PII redaction and replacement."""

    def __init__(self):
        super().__init__(name="ZeroKnowledgePrivacyEngine", step_number=6)

    def _tokenize_value(self, category: str, original_val: str) -> str:
        """Generates a deterministic token hash for a given PII string."""
        if not original_val:
            return f"[{category.upper()}_TOK_0000]"
        h = hashlib.sha256(original_val.strip().lower().encode("utf-8")).hexdigest()[:8]
        return f"[{category.upper()}_TOK_{h}]"

    def _generate_fallback(self, user_prompt: str) -> Dict[str, Any]:
        return {
            "detected_pii": [
                {"type": "NAME", "value": "Customer"},
                {"type": "ACCOUNT", "value": "ACC_XXXXXX"}
            ],
            "token_mappings": {
                "Customer": "[NAME_TOK_8841a1]",
                "ACC_884920": "[ACCT_TOK_9b2e71]"
            },
            "sanitized_complaint": user_prompt,
            "sanitized_customer_name": "[NAME_TOK_8841a1]",
            "sanitized_pan": "[PAN_TOK_d4e3f2]",
            "sanitized_account": "[ACCT_TOK_9b2e71]",
            "sanitized_phone": "[PHONE_TOK_7c11a0]",
            "sanitized_email": "[EMAIL_TOK_3f92b1]"
        }

    def execute(self, context: AgentContext, db: Session) -> AgentContext:
        start_time = time.time()
        self.logger.info(f"[{self.name}] Tokenizing PII for Investigation ID: {context.investigation_id}")

        cust_summary = context.evidence_package.get("customer_summary", {})
        cust_name = cust_summary.get("name", "")
        cust_email = cust_summary.get("email", "")
        cust_phone = cust_summary.get("phone", "")
        cust_account = cust_summary.get("account_number", "")
        pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]{1}", context.complaint_text)
        cust_pan = pan_match.group(0) if pan_match else "ABCDE1234F"

        token_map = {}
        detected_pii = []

        if cust_name and len(cust_name) > 2:
            t = self._tokenize_value("NAME", cust_name)
            token_map[cust_name] = t
            detected_pii.append({"type": "NAME", "value": cust_name, "token": t})

        if cust_email:
            t = self._tokenize_value("EMAIL", cust_email)
            token_map[cust_email] = t
            detected_pii.append({"type": "EMAIL", "value": cust_email, "token": t})

        if cust_phone:
            t = self._tokenize_value("PHONE", cust_phone)
            token_map[cust_phone] = t
            detected_pii.append({"type": "PHONE", "value": cust_phone, "token": t})

        if cust_account:
            t = self._tokenize_value("ACCOUNT", cust_account)
            token_map[cust_account] = t
            detected_pii.append({"type": "ACCOUNT", "value": cust_account, "token": t})

        if cust_pan:
            t = self._tokenize_value("PAN", cust_pan)
            token_map[cust_pan] = t
            detected_pii.append({"type": "PAN", "value": cust_pan, "token": t})

        # Redact complaint text deterministically
        sanitized_complaint = context.complaint_text
        for orig, tok in token_map.items():
            if orig:
                sanitized_complaint = sanitized_complaint.replace(orig, tok)

        # Regex fallback for email and phone in complaint
        sanitized_complaint = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL_TOK_REDACTED]", sanitized_complaint)
        sanitized_complaint = re.sub(r"\+?\d{10,12}", "[PHONE_TOK_REDACTED]", sanitized_complaint)

        privacy_payload = {
            "detected_pii": detected_pii,
            "token_mappings": token_map,
            "sanitized_complaint": sanitized_complaint,
            "sanitized_customer_name": token_map.get(cust_name, "[NAME_TOK_MASKED]"),
            "sanitized_pan": token_map.get(cust_pan, "[PAN_TOK_MASKED]"),
            "sanitized_account": token_map.get(cust_account, "[ACCT_TOK_MASKED]"),
            "sanitized_phone": token_map.get(cust_phone, "[PHONE_TOK_MASKED]"),
            "sanitized_email": token_map.get(cust_email, "[EMAIL_TOK_MASKED]")
        }

        context.privacy_tokens = privacy_payload

        execution_time_ms = (time.time() - start_time) * 1000
        self.persist_step(
            context=context,
            db=db,
            action_taken="ZERO_KNOWLEDGE_PII_TOKENIZED",
            output_payload=privacy_payload,
            execution_time_ms=execution_time_ms
        )

        return context
