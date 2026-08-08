from typing import Dict, Any
from backend.config import settings


# In-memory settings store initialized from app settings
SYSTEM_SETTINGS: Dict[str, Any] = {
    "models": {
        "primary_model": getattr(settings, "GROQ_MODEL", "llama-3.3-70b-versatile"),
        "fallback_model": "llama-3.1-8b-instant",
        "embedding_model": "all-MiniLM-L6-v2"
    },
    "temperature": {
        "default_temperature": 0.1,
        "decision_temperature": 0.2,
        "zero_trust_temperature": 0.0
    },
    "privacy": {
        "pii_shield_enabled": True,
        "deterministic_tokenization": True,
        "mask_customer_names": True,
        "mask_pan_and_accounts": True
    },
    "rag": {
        "top_k_chunks": 5,
        "similarity_threshold": 0.70,
        "chunk_size": 512,
        "chunk_overlap": 50
    },
    "thresholds": {
        "auto_approval_limit_inr": 10000.0,
        "high_risk_fraud_score_threshold": 0.70,
        "min_decision_confidence": 0.85,
        "max_zero_trust_revisions": 1
    }
}


class SettingsService:
    """Service layer managing system settings configuration."""

    @staticmethod
    def get_settings() -> Dict[str, Any]:
        return SYSTEM_SETTINGS

    @staticmethod
    def update_settings(payload: Dict[str, Any]) -> Dict[str, Any]:
        global SYSTEM_SETTINGS
        for category, vals in payload.items():
            if category in SYSTEM_SETTINGS and isinstance(vals, dict):
                SYSTEM_SETTINGS[category].update(vals)
            else:
                SYSTEM_SETTINGS[category] = vals
        return SYSTEM_SETTINGS
