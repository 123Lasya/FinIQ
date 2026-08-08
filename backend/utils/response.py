from typing import Any
from datetime import datetime
from fastapi.responses import JSONResponse


def api_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
    success: bool = True
) -> JSONResponse:
    """Standardized API response wrapper returning { success, message, data, timestamp }."""
    payload = {
        "success": success,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return JSONResponse(status_code=status_code, content=payload)
