import json
import time
import hashlib
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.config import settings
from backend.logging import logger
from backend.schemas.agent import AgentContext, AgentExecutionResult
from backend.prompts.agent_prompts import AGENT_SYSTEM_PROMPTS


class BaseAgent(ABC):
    """Abstract base class for all FinPilot AI agents."""

    def __init__(self, name: str, step_number: int):
        self.name = name
        self.step_number = step_number
        self.system_prompt = AGENT_SYSTEM_PROMPTS.get(name, "")
        self.groq_api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self._groq_client = None
        self._init_client()

    def _init_client(self):
        if self.groq_api_key and self.groq_api_key.startswith("gsk_"):
            try:
                from groq import Groq
                self._groq_client = Groq(api_key=self.groq_api_key)
                logger.info(f"Initialized Groq LLM client for agent: {self.name}")
            except Exception as e:
                logger.warning(f"Groq client init warning for {self.name}: {e}")
                self._groq_client = None
        else:
            logger.info(f"Groq API key not configured or using standard fallback for agent: {self.name}")

    def call_llm(self, user_prompt: str, temperature: float = 0.1) -> str:
        """Calls Groq LLM or falls back to rule-based generation if offline."""
        if self._groq_client is not None:
            try:
                response = self._groq_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=settings.GROQ_MAX_TOKENS,
                    response_format={"type": "json_object"}
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"Groq LLM call error in agent {self.name}: {e}")

        # Rule-based fallback if GROQ is unreachable or API key missing
        return self._generate_fallback_response(user_prompt)

    @abstractmethod
    def _generate_fallback_response(self, user_prompt: str) -> str:
        """Rule-based JSON output when LLM API is unavailable."""
        pass

    @abstractmethod
    def execute(self, context: AgentContext, db: Session) -> AgentExecutionResult:
        """Executes agent task and returns AgentExecutionResult."""
        pass

    def compute_hash(self, input_data: str, output_data: str) -> str:
        """Generates SHA-256 hash signature for audit logging."""
        timestamp = str(time.time())
        raw = f"{self.name}:{self.step_number}:{input_data}:{output_data}:{timestamp}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
