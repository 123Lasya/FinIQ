import enum


class EmployeeRole(str, enum.Enum):
    OPERATIONS_EXEC = "OPERATIONS_EXEC"
    CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT"
    FRAUD_ANALYST = "FRAUD_ANALYST"
    COMPLIANCE_OFFICER = "COMPLIANCE_OFFICER"


class CustomerRiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TransactionType(str, enum.Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    TRANSFER = "TRANSFER"


class TransactionStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"
    DISPUTED = "DISPUTED"


class InvestigationIssueType(str, enum.Enum):
    DOUBLE_CHARGE = "DOUBLE_CHARGE"
    UNAUTHORIZED_TRANSACTION = "UNAUTHORIZED_TRANSACTION"
    FAILED_TRANSFER = "FAILED_TRANSFER"
    FEE_DISPUTE = "FEE_DISPUTE"
    ACCOUNT_TAKEOVER = "ACCOUNT_TAKEOVER"
    GENERAL_COMPLAINT = "GENERAL_COMPLAINT"


class InvestigationPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class InvestigationStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    AUTO_EXECUTED = "AUTO_EXECUTED"
    REQUIRES_HUMAN_APPROVAL = "REQUIRES_HUMAN_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class EmbeddingStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AgentExecutionStatus(str, enum.Enum):
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ComplianceStatus(str, enum.Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    FLAGGED_HUMAN_REVIEW = "FLAGGED_HUMAN_REVIEW"
