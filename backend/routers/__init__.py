from backend.routers.auth import router as auth_router
from backend.routers.investigations import router as investigations_router
from backend.routers.dashboard import router as dashboard_router
from backend.routers.knowledge import router as knowledge_router
from backend.routers.approvals import router as approvals_router
from backend.routers.reports import router as reports_router
from backend.routers.analytics import router as analytics_router
from backend.routers.settings import router as settings_router
from backend.routers.rag import router as rag_router
from backend.routers.audit import router as audit_router
from backend.routers.policy import router as policy_router

__all__ = [
    "auth_router",
    "investigations_router",
    "dashboard_router",
    "knowledge_router",
    "approvals_router",
    "reports_router",
    "analytics_router",
    "settings_router",
    "rag_router",
    "audit_router",
    "policy_router",
]
