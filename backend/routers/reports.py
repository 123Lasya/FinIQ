from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.utils.deps import get_current_active_user
from backend.services.report_service import ReportService
from backend.utils.response import api_response

router = APIRouter(prefix="/reports", tags=["Investigation Audit Reports"])
report_service = ReportService()


@router.get("")
@router.get("/")
def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves list of generated investigation audit reports."""
    reports = report_service.list_reports(db)
    return api_response(
        data=reports,
        message=f"Retrieved {len(reports)} investigation reports.",
        status_code=status.HTTP_200_OK
    )


@router.get("/{id}")
def get_report_detail(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retrieves detailed investigation report with multi-agent logs and audit hashes."""
    detail = report_service.get_report_detail(db, id)
    return api_response(
        data=detail,
        message="Investigation report detail retrieved successfully.",
        status_code=status.HTTP_200_OK
    )


@router.get("/{id}/export")
def export_report_pdf(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generates and exports formal PDF audit report."""
    exported = report_service.export_pdf_report(db, id)
    return api_response(
        data=exported,
        message=f"PDF report '{exported['filename']}' generated successfully.",
        status_code=status.HTTP_200_OK
    )
