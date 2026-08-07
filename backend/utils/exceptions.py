class FinPilotException(Exception):
    """Base exception for all FinPilot AI backend domain errors."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ResourceNotFoundException(FinPilotException):
    """Raised when a requested database entity or file is not found."""

    def __init__(self, resource_name: str, resource_id: str):
        message = f"{resource_name} with key '{resource_id}' was not found."
        super().__init__(message, status_code=404)


class ComplianceViolationException(FinPilotException):
    """Raised when a financial operation violates policy guardrails."""

    def __init__(self, violation_reason: str):
        message = f"Compliance Policy Violation: {violation_reason}"
        super().__init__(message, status_code=400)


class AuthenticationException(FinPilotException):
    """Raised when employee credentials or token validation fails."""

    def __init__(self, detail: str = "Invalid employee credentials"):
        super().__init__(detail, status_code=401)
