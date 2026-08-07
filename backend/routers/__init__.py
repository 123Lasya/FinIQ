from backend.routers.auth import router as auth_router
from backend.routers.investigations import router as investigations_router
from backend.routers.rag import router as rag_router
from backend.routers.audit import router as audit_router
from backend.routers.analytics import router as analytics_router
from backend.routers.policy import router as policy_router

__all__ = [
    "auth_router",
    "investigations_router",
    "rag_router",
    "audit_router",
    "analytics_router",
    "policy_router",
]
