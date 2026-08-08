from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.services.analytics_service import AnalyticsService
from backend.utils.response import api_response

router = APIRouter(prefix="/analytics", tags=["System & Operations Analytics"])
analytics_service = AnalyticsService()


@router.get("")
@router.get("/")
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves system analytics: charts, confidence breakdown, overrides, fraud categories, agent runtimes, simulation results, and policy usage."""
    data = analytics_service.get_analytics_metrics(db)
    return api_response(
        data=data,
        message="Analytics metrics retrieved successfully.",
        status_code=status.HTTP_200_OK
    )
