from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.policy import PolicyRule
from backend.schemas.policy import PolicySchema, PolicyCheckResult
from backend.config import settings


class PolicyService:
    """Service managing compliance policy rules."""

    @staticmethod
    def get_all_policies(db: Session) -> List[PolicyRule]:
        return db.query(PolicyRule).all()

    @staticmethod
    def create_policy(db: Session, payload: PolicySchema) -> PolicyRule:
        rule = PolicyRule(
            policy_code=payload.policy_code,
            title=payload.title,
            description=payload.description,
            max_refund_limit=payload.max_refund_limit,
            requires_compliance_review=payload.requires_compliance_review,
            is_active=payload.is_active
        )
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule

    @staticmethod
    def evaluate_amount_compliance(amount: float) -> PolicyCheckResult:
        max_limit = settings.AUTO_APPROVAL_THRESHOLD_INR
        violations = []
        requires_human = False

        if amount > max_limit:
            violations.append(f"Dispute amount ₹{amount:,.2f} exceeds threshold ₹{max_limit:,.2f}")
            requires_human = True

        return PolicyCheckResult(
            passed=(len(violations) == 0),
            violations=violations,
            max_allowed_refund=max_limit,
            requires_human_signoff=requires_human
        )
