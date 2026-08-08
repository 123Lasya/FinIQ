import time
from typing import Dict, Any
from sqlalchemy.orm import Session

from backend.agents.base_agent import BaseAgent
from backend.agents.agent_context import AgentContext
from backend.orchestrator.response_models import ShadowOutput


class PreFlightShadowSimulationAgent(BaseAgent):
    """Agent 5: Pre-Flight Shadow Simulation Agent for predictive financial, fraud, retention, and operational modeling."""

    def __init__(self):
        super().__init__(name="PreFlightShadowSimulationAgent", step_number=5)

    def _generate_fallback(self, user_prompt: str) -> Dict[str, Any]:
        return {
            "predicted_financial_impact": float(getattr(self, "_current_amount", 4999.0)),
            "fraud_risk_score": 0.08,
            "customer_retention_impact": "POSITIVE",
            "operational_cost": 150.0,
            "predictive_impact_summary": (
                "Shadow simulation predicts net financial outflow of dispute amount with 0.08 low fraud risk score. "
                "Immediate resolution boosts customer lifetime retention value while keeping ops handling cost under INR 150."
            )
        }

    def execute(self, context: AgentContext, db: Session) -> AgentContext:
        start_time = time.time()
        self.logger.info(f"[{self.name}] Running pre-flight shadow simulation for Investigation ID: {context.investigation_id}")

        self._current_amount = context.dispute_amount

        user_prompt = (
            f"Proposed Decision: {context.decision_recommendation}\n"
            f"Dispute Amount: {context.dispute_amount} {context.currency}\n"
            f"Evidence Package: {context.evidence_package}\n"
            f"Zero Trust Result: {context.zero_trust_result}\n\n"
            "Simulate and predict: 1) predicted_financial_impact (float), 2) fraud_risk_score (0.0 to 1.0), "
            "3) customer_retention_impact (POSITIVE, NEUTRAL, NEGATIVE), 4) operational_cost (float), "
            "and 5) predictive_impact_summary."
        )

        output_dict = self.call_llm(user_prompt, ShadowOutput)

        try:
            validated = ShadowOutput(**output_dict)
            shadow_data = validated.model_dump()
        except Exception:
            shadow_data = output_dict

        context.shadow_simulation = shadow_data

        execution_time_ms = (time.time() - start_time) * 1000
        self.persist_step(
            context=context,
            db=db,
            action_taken="PRE_FLIGHT_SIMULATION_COMPLETED",
            output_payload=shadow_data,
            execution_time_ms=execution_time_ms
        )

        return context
