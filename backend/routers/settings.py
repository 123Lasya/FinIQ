from typing import Dict, Any
from fastapi import APIRouter, Depends, Body, status
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.services.settings_service import SettingsService
from backend.utils.response import api_response

router = APIRouter(prefix="/settings", tags=["System Settings"])
settings_service = SettingsService()


@router.get("")
@router.get("/")
def get_system_settings(current_user: User = Depends(get_current_active_user)):
    """Retrieves current AI model configurations, temperatures, privacy, RAG, and approval thresholds."""
    current_settings = settings_service.get_settings()
    return api_response(
        data=current_settings,
        message="System settings retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.put("")
@router.put("/")
def update_system_settings(
    payload: Dict[str, Any] = Body(...),
    current_user: User = Depends(get_current_active_user)
):
    """Updates system settings for models, temperature, privacy, RAG, and thresholds."""
    updated = settings_service.update_settings(payload)
    return api_response(
        data=updated,
        message="System settings updated successfully.",
        status_code=status.HTTP_200_OK
    )
