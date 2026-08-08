import json
import time
import hashlib
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from backend.logging import logger
from backend.agents.agent_context import AgentContext
from backend.orchestrator.prompt_manager import PromptManager
from backend.orchestrator.groq_client import groq_client
from backend.models import AgentExecutionLog, AgentArtifact, Investigation, AuditLog
from backend.models.enums import AgentExecutionStatus, InvestigationStatus


class BaseAgent(ABC):
    """Abstract Base Class for all FinPilot AI Backend Agents."""

    def __init__(self, name: str, step_number: int):
        self.name = name
        self.step_number = step_number
        self.logger = logger
        
        config = PromptManager.get_agent_config(name)
        self.system_prompt = config["system_prompt"]
        self.model = config["model"]
        self.temperature = config["temperature"]
        self.max_tokens = config["max_tokens"]

    def call_llm(self, user_prompt: str, response_model=None) -> Dict[str, Any]:
        """Calls Groq LLM using OpenAI-compatible interface with fallback to deterministic response."""
        res = groq_client.generate_json(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        if res:
            return res

        return self._generate_fallback(user_prompt)

    @abstractmethod
    def _generate_fallback(self, user_prompt: str) -> Dict[str, Any]:
        """Rule-based fallback response if Groq API is offline or unconfigured."""
        pass

    @abstractmethod
    def execute(self, context: AgentContext, db: Session) -> AgentContext:
        """Executes agent logic, updates context, and returns modified AgentContext."""
        pass

    def compute_hash(self, input_data: str, output_data: str) -> str:
        """Generates SHA-256 cryptographic hash signature for audit tracking."""
        timestamp = str(time.time())
        raw = f"{self.name}:{self.step_number}:{input_data}:{output_data}:{timestamp}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def persist_step(
        self,
        context: AgentContext,
        db: Session,
        action_taken: str,
        output_payload: Dict[str, Any],
        execution_time_ms: float,
        status: AgentExecutionStatus = AgentExecutionStatus.SUCCESS
    ):
        """Immediately persists step execution log and artifact to MySQL database to support 1s frontend polling."""
        try:
            # 1. Update Agent Execution Logs
            exec_log = AgentExecutionLog(
                investigation_id=context.investigation_id,
                agent_name=self.name,
                status=status,
                execution_time=round(execution_time_ms / 1000.0, 3),
                confidence=float(context.decision_recommendation.get("confidence", 1.0)),
                model_used=self.model,
                started_at=datetime.utcnow(),
                completed_at=datetime.utcnow()
            )
            db.add(exec_log)

            # 2. Update Agent Artifacts
            artifact = AgentArtifact(
                investigation_id=context.investigation_id,
                agent_name=self.name,
                artifact_type=f"{self.name}_output",
                artifact_json=json.dumps(output_payload)
            )
            db.add(artifact)

            # 3. Update Investigation state
            inv = db.query(Investigation).filter(Investigation.investigation_id == context.investigation_id).first()
            if inv:
                inv.current_agent = self.name
                if self.name == "DecisionIntelligenceAgent":
                    inv.final_decision = context.decision_recommendation.get("recommendation")
                    inv.decision_type = context.decision_recommendation.get("suggested_action")
                elif self.name == "ExecutionAgent":
                    if context.policy_evaluation.get("status") == "AUTO":
                        inv.status = InvestigationStatus.AUTO_EXECUTED
                    else:
                        inv.status = InvestigationStatus.REQUIRES_HUMAN_APPROVAL

            # 4. Record step log telemetry in memory context
            step_log = {
                "agent_name": self.name,
                "step_number": self.step_number,
                "action": action_taken,
                "output": output_payload,
                "execution_time_ms": execution_time_ms,
                "timestamp": datetime.utcnow().isoformat()
            }
            context.agent_logs.append(step_log)
            context.current_agent = self.name

            db.commit()
            self.logger.info(f"[{self.name}] DB persisted step {self.step_number} in {execution_time_ms:.2f}ms")
        except Exception as e:
            db.rollback()
            self.logger.error(f"[{self.name}] Error persisting agent step to DB: {e}")
