from backend.repositories.base import BaseRepository
from backend.repositories.investigation_repository import InvestigationRepository
from backend.repositories.customer_repository import CustomerRepository
from backend.repositories.transaction_repository import TransactionRepository
from backend.repositories.approval_repository import ApprovalRepository
from backend.repositories.audit_repository import AuditRepository
from backend.repositories.document_repository import DocumentRepository
from backend.repositories.employee_repository import EmployeeRepository

__all__ = [
    "BaseRepository",
    "InvestigationRepository",
    "CustomerRepository",
    "TransactionRepository",
    "ApprovalRepository",
    "AuditRepository",
    "DocumentRepository",
    "EmployeeRepository",
]
