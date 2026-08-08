from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.config import settings
from backend.logging import logger
from backend.database import init_db
from backend.demo_data.seed_data import seed_database
from backend.middleware import (
    RequestLoggingMiddleware,
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler
)
from backend.routers import (
    auth_router,
    investigations_router,
    dashboard_router,
    knowledge_router,
    approvals_router,
    reports_router,
    analytics_router,
    settings_router,
    rag_router,
    audit_router,
    policy_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle event handler."""
    logger.info(f"Starting {settings.PROJECT_NAME} (v{settings.VERSION})...")
    try:
        init_db()
        seed_database()
    except Exception as e:
        logger.warning(f"Startup initialization notice: {e}")
    yield
    logger.info("Shutting down FinPilot AI application...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Multi-Agent Financial Operations Assistant Backend Engine",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

frontend_path = Path(__file__).resolve().parent.parent / "frontend"

# 1. Custom Middlewares
app.add_middleware(RequestLoggingMiddleware)

# 2. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, "BACKEND_CORS_ORIGINS", ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Custom Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 4. Register API Routers under /api
api_prefix = settings.API_V1_STR  # "/api"
app.include_router(auth_router, prefix=api_prefix)
app.include_router(investigations_router, prefix=api_prefix)
app.include_router(dashboard_router, prefix=api_prefix)
app.include_router(knowledge_router, prefix=api_prefix)
app.include_router(approvals_router, prefix=api_prefix)
app.include_router(reports_router, prefix=api_prefix)
app.include_router(analytics_router, prefix=api_prefix)
app.include_router(settings_router, prefix=api_prefix)
app.include_router(rag_router, prefix=api_prefix)
app.include_router(audit_router, prefix=api_prefix)
app.include_router(policy_router, prefix=api_prefix)


@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(frontend_path / "index.html")


@app.get("/health", tags=["System Readiness"])
def health_check():
    return {"status": "HEALTHY", "environment": getattr(settings, "ENVIRONMENT", "production")}


app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/{full_path:path}", include_in_schema=False)
def serve_frontend_fallback(full_path: str):
    requested_path = frontend_path / full_path
    if requested_path.exists() and requested_path.is_file():
        return FileResponse(requested_path)
    return FileResponse(frontend_path / "index.html")
