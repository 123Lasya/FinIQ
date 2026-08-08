import uuid
import time
from typing import Dict, Any, List, Optional
from backend.logging import logger


class MockCRMService:
    """Mock Enterprise CRM Service for customer profile & history lookup."""

    @staticmethod
    def get_customer_profile(customer_id: str) -> Dict[str, Any]:
        logger.info(f"[MockCRM] Querying core CRM for customer_id={customer_id}")
        return {
            "crm_id": f"CRM_{customer_id[:8]}",
            "kyc_status": "VERIFIED",
            "tier": "PLATINUM",
            "lifetime_disputes_count": 1,
            "account_health": "EXCELLENT",
            "relationship_score": 98.5
        }


class MockPaymentGatewayService:
    """Mock Payment Gateway Service for transaction verification and refund reversals."""

    @staticmethod
    def verify_transaction_status(transaction_id: str) -> Dict[str, Any]:
        logger.info(f"[MockGateway] Querying payment gateway for txn_id={transaction_id}")
        return {
            "gateway_ref": f"PG_REF_{transaction_id}",
            "status": "SETTLED",
            "network": "VISA_DIRECT",
            "auth_code": "AUTH_998412",
            "response_code": "00_SUCCESS"
        }

    @staticmethod
    def process_credit_reversal(account_number: str, amount: float, currency: str = "INR") -> Dict[str, Any]:
        logger.info(f"[MockGateway] Executing credit reversal of {amount} {currency} to {account_number}")
        return {
            "settlement_id": f"SETTLE_{uuid.uuid4().hex[:10].upper()}",
            "amount_credited": amount,
            "currency": currency,
            "status": "COMPLETED",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }


class MockFraudEngineService:
    """Mock Enterprise Fraud Engine for risk score calculation."""

    @staticmethod
    def evaluate_risk_signals(customer_id: str, amount: float, merchant: str) -> Dict[str, Any]:
        logger.info(f"[MockFraudEngine] Evaluating risk for customer={customer_id}, amount={amount}, merchant={merchant}")
        is_high_value = amount > 50000
        return {
            "risk_score": 0.35 if is_high_value else 0.08,
            "is_blacklisted_ip": False,
            "is_blacklisted_device": False,
            "geo_velocity_flag": False,
            "merchant_risk_tier": "MEDIUM" if is_high_value else "LOW"
        }


class MockNotificationService:
    """Mock Notification Service for dispatching customer/employee alerts."""

    @staticmethod
    def send_dispute_update(customer_id: str, email: str, status: str, message: str) -> bool:
        logger.info(f"[MockNotification] Dispatching SMS/Email alert to {email} (status={status}): {message}")
        return True


class MockLedgerService:
    """Mock Core Banking Double-Entry Ledger Service."""

    @staticmethod
    def post_dispute_entry(investigation_id: str, amount: float, debit_acct: str, credit_acct: str) -> Dict[str, Any]:
        logger.info(f"[MockLedger] Posting double-entry ledger record for Inv: {investigation_id}, Amount: {amount}")
        return {
            "ledger_batch_id": f"BATCH_{uuid.uuid4().hex[:8]}",
            "debit_account": debit_acct,
            "credit_account": credit_acct,
            "posted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "BALANCED_AND_POSTED"
        }
