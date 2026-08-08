from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class AgentContext(BaseModel):
    """Standard unified context object passed through and updated by all 9 agents."""

    investigation_id: str
    token_id: str
    customer_id: str
    complaint_text: str = Field(alias="customer_complaint", default="")
    dispute_amount: float = 0.0
    currency: str = "INR"

    # Agent 1 Output
    structured_investigation: Dict[str, Any] = Field(default_factory=dict)

    # Agent 2 Output
    evidence_package: Dict[str, Any] = Field(default_factory=dict)

    # Agent 3 Output
    decision_recommendation: Dict[str, Any] = Field(default_factory=dict)

    # Agent 4 Output & Revision Control
    zero_trust_result: Dict[str, Any] = Field(default_factory=dict)
    revision_count: int = 0
    skip_zero_trust: bool = False

    # Agent 5 Output
    shadow_simulation: Dict[str, Any] = Field(default_factory=dict)

    # Agent 6 Output
    privacy_tokens: Dict[str, Any] = Field(default_factory=dict)

    # Agent 7 Output
    policy_evaluation: Dict[str, Any] = Field(default_factory=dict)

    # Agent 8 Output
    execution_result: Dict[str, Any] = Field(default_factory=dict)

    # Agent 9 Output
    audit_trail: Dict[str, Any] = Field(default_factory=dict)

    # Telemetry and Execution Tracking
    agent_logs: List[Dict[str, Any]] = Field(default_factory=list)
    current_agent: Optional[str] = None
    status: str = "PENDING"
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        populate_by_name = True

    # Accessor helper properties for backward compatibility
    @property
    def customer_complaint(self) -> str:
        return self.complaint_text

    @property
    def redacted_text(self) -> Optional[str]:
        return self.privacy_tokens.get("sanitized_complaint")

    @property
    def recommended_decision(self) -> Optional[str]:
        return self.decision_recommendation.get("recommendation")

    @property
    def confidence_score(self) -> float:
        return float(self.decision_recommendation.get("confidence", 0.0))

    @property
    def reasoning(self) -> Optional[str]:
        return self.decision_recommendation.get("financial_reasoning") or self.decision_recommendation.get("explanation")

    @property
    def human_approval_required(self) -> bool:
        return self.policy_evaluation.get("status") in ["HUMAN", "BLOCK"] or self.execution_result.get("execution_type") == "HUMAN_APPROVAL_REQUESTED"

    @property
    def auto_executed(self) -> bool:
        return self.policy_evaluation.get("status") == "AUTO" or self.execution_result.get("execution_type") == "AUTO_EXECUTED"

    @property
    def zero_trust_validated(self) -> bool:
        return self.zero_trust_result.get("status") == "PASS"
