from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.services.dashboard_service import DashboardService
from backend.utils.response import api_response

router = APIRouter(prefix="/dashboard", tags=["Operations Dashboard"])
dashboard_service = DashboardService()


@router.get("")
@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves enterprise operations dashboard metrics, counters, activity stream, and charts."""
    metrics = dashboard_service.get_dashboard_metrics(db)
    return api_response(
        data=metrics,
        message="Dashboard telemetry retrieved successfully.",
        status_code=status.HTTP_200_OK
    )
