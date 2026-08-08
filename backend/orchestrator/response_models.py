from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class IntakeOutput(BaseModel):
    intent: str = Field(..., description="Detected intent of the customer complaint")
    priority: str = Field(..., description="Calculated priority: LOW, MEDIUM, HIGH, CRITICAL")
    classification: str = Field(..., description="Issue classification type")
    extracted_entities: Dict[str, Any] = Field(default_factory=dict, description="Extracted key entities (amount, date, merchant, etc.)")
    summary: str = Field(..., description="Brief summary of intake finding")


class ContextOutput(BaseModel):
    customer_summary: Dict[str, Any] = Field(default_factory=dict, description="Retrieved customer profile details")
    transactions_summary: List[Dict[str, Any]] = Field(default_factory=list, description="Retrieved transaction history")
    fraud_history_summary: List[Dict[str, Any]] = Field(default_factory=list, description="Retrieved fraud markers")
    previous_cases_summary: List[Dict[str, Any]] = Field(default_factory=list, description="Historical customer dispute cases")
    rag_chunks: List[Dict[str, Any]] = Field(default_factory=list, description="Top 5 RAG knowledge base chunks")
    evidence_completeness: float = Field(default=1.0, description="Completeness score of gathered context (0.0 to 1.0)")
    risk_signals: List[str] = Field(default_factory=list, description="Identified risk indicators")


class DecisionOutput(BaseModel):
    financial_reasoning: str = Field(..., description="Financial logic and policy reasoning behind decision")
    recommendation: str = Field(..., description="Recommended action: FULL_REFUND, PARTIAL_REFUND, REJECT_CLAIM, REQUIRE_ADDITIONAL_DOCS, FLAG_FRAUD")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")
    explanation: str = Field(..., description="Detailed explanation for customer & ops team")
    suggested_action: str = Field(..., description="Specific recommended operational action")


class ZeroTrustOutput(BaseModel):
    status: str = Field(..., description="PASS or REVISE")
    evidence_validation_passed: bool = Field(default=True, description="Whether evidence supports decision")
    prompt_injection_detected: bool = Field(default=False, description="Whether prompt injection attempt was flagged")
    contradiction_detected: bool = Field(default=False, description="Whether internal contradictions exist")
    alternative_hypothesis: Optional[str] = Field(None, description="Alternative plausible explanation")
    missing_information: List[str] = Field(default_factory=list, description="List of missing evidence fields")
    confidence_validated: bool = Field(default=True, description="Whether confidence score is justified")
    revision_feedback: Optional[str] = Field(None, description="Actionable feedback for Agent 3 if REVISE")
    security_findings: List[str] = Field(default_factory=list, description="Detailed security audit notes")


class ShadowOutput(BaseModel):
    predicted_financial_impact: float = Field(..., description="Predicted financial impact in INR")
    fraud_risk_score: float = Field(..., description="Predicted fraud risk score (0.0 - 1.0)")
    customer_retention_impact: str = Field(..., description="POSITIVE, NEUTRAL, or NEGATIVE")
    operational_cost: float = Field(..., description="Estimated operational handling cost")
    predictive_impact_summary: str = Field(..., description="Executive summary of pre-flight simulation")


class PrivacyOutput(BaseModel):
    detected_pii: List[Dict[str, str]] = Field(default_factory=list, description="List of detected PII items")
    token_mappings: Dict[str, str] = Field(default_factory=dict, description="PII -> Deterministic Token mapping")
    sanitized_complaint: str = Field(..., description="Complaint text with PII replaced by tokens")
    sanitized_customer_name: str = Field(default="[CUSTOMER_NAME_TOKEN]")
    sanitized_pan: str = Field(default="[PAN_TOKEN]")
    sanitized_account: str = Field(default="[ACCOUNT_TOKEN]")
    sanitized_phone: str = Field(default="[PHONE_TOKEN]")
    sanitized_email: str = Field(default="[EMAIL_TOKEN]")


class GuardrailOutput(BaseModel):
    status: str = Field(..., description="AUTO, HUMAN, or BLOCK")
    refund_policy_check: bool = Field(default=True)
    rbi_compliance_check: bool = Field(default=True)
    fraud_sop_check: bool = Field(default=True)
    internal_rules_check: bool = Field(default=True)
    violations: List[str] = Field(default_factory=list)
    reason: str = Field(..., description="Detailed policy compliance rationale")


class ExecutionOutput(BaseModel):
    execution_type: str = Field(..., description="AUTO_EXECUTED or HUMAN_APPROVAL_REQUESTED")
    execution_summary: str = Field(..., description="Summary of execution outcome")
    approval_details: Optional[Dict[str, Any]] = Field(None, description="Details if sent to approval queue")
    status: str = Field(..., description="Final status: AUTO_EXECUTED, REQUIRES_HUMAN_APPROVAL, REJECTED")


class AuditOutput(BaseModel):
    audit_hash: str = Field(..., description="SHA-256 integrity hash of investigation trace")
    compliance_summary: str = Field(..., description="Compliance verification summary")
    reasoning_trace: str = Field(..., description="Full chain-of-thought reasoning audit trail")
    verified: bool = Field(default=True)
    remarks: str = Field(..., description="Final audit record remarks")
