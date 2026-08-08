from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from backend.logging import logger
from backend.utils.response import api_response


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global Exception Handler capturing all uncaught server errors (500)."""
    logger.error(f"Global Exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return api_response(
        data={"error_details": str(exc)},
        message="An unexpected internal server error occurred in FinPilot AI backend.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        success=False
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Captures FastAPI HTTPExceptions (400, 401, 403, 404, 422)."""
    logger.warning(f"HTTPException [{exc.status_code}] on {request.method} {request.url.path}: {exc.detail}")
    return api_response(
        data=None,
        message=str(exc.detail),
        status_code=exc.status_code,
        success=False
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Captures request validation errors (422)."""
    logger.warning(f"ValidationError on {request.method} {request.url.path}: {exc.errors()}")
    return api_response(
        data={"validation_errors": exc.errors()},
        message="Request payload validation failed.",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        success=False
    )
