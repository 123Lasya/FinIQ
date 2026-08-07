from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AgentContext(BaseModel):
    token_id: str
    customer_id: str
    complaint_text: str
    redacted_text: Optional[str] = None
    dispute_amount: float = 0.0
    currency: str = "INR"
    extracted_entities: Dict[str, Any] = Field(default_factory=dict)
    retrieved_policies: List[Dict[str, Any]] = Field(default_factory=list)
    customer_history: List[Dict[str, Any]] = Field(default_factory=list)
    recommended_decision: Optional[str] = None
    confidence_score: float = 0.0
    reasoning: Optional[str] = None
    zero_trust_validated: bool = False
    zero_trust_findings: List[str] = Field(default_factory=list)
    shadow_simulation_passed: bool = False
    shadow_simulation_details: Dict[str, Any] = Field(default_factory=dict)
    policy_guardrail_passed: bool = False
    policy_violations: List[str] = Field(default_factory=list)
    human_approval_required: bool = False
    auto_executed: bool = False
    execution_result: Optional[Dict[str, Any]] = None
    audit_report: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentExecutionResult(BaseModel):
    agent_name: str
    step_number: int
    success: bool
    action_taken: str
    output_data: Dict[str, Any]
    execution_time_ms: float
    hash_signature: str


class AgentStepLog(BaseModel):
    agent_name: str
    step_number: int
    action: str
    input_summary: str
    output_summary: str
    execution_time_ms: float
    hash_signature: str
    created_at: datetime


class AuditReportSchema(BaseModel):
    token_id: str
    status: str
    total_steps: int
    agent_logs: List[AgentStepLog]
    final_decision: Optional[str]
    confidence_score: float
    auto_executed: bool
    human_approval_required: bool
    compliance_passed: bool
    integrity_hash: str
