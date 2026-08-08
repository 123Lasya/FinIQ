import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for injecting X-Request-ID and logging request execution timing."""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.time()

        logger.info(f"--> [{request_id[:8]}] {request.method} {request.url.path}")

        try:
            response = await call_next(request)
            process_time = round((time.time() - start_time) * 1000, 2)
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time}ms"

            logger.info(f"<-- [{request_id[:8]}] {request.method} {request.url.path} - Status: {response.status_code} ({process_time}ms)")
            return response
        except Exception as exc:
            process_time = round((time.time() - start_time) * 1000, 2)
            logger.error(f"x-- [{request_id[:8]}] Exception on {request.method} {request.url.path}: {exc} ({process_time}ms)")
            raise exc
