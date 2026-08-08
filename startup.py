#!/usr/bin/env python
"""Complete project bootstrap script: initializes DB tables, seeds demo data, and starts uvicorn server."""
import sys
import os
import uvicorn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import init_db
from backend.demo_data.seed_data import seed_database
from backend.logging import logger
from backend.config import settings

def main():
    print("=" * 60)
    print(f"BOOTSTRAPPING {settings.PROJECT_NAME} BACKEND ENGINE")
    print("=" * 60)

    # 1. Init DB Tables
    logger.info("[Startup] Creating database tables...")
    init_db()
    print("✓ Database tables created.")

    # 2. Seed Demo Data
    logger.info("[Startup] Seeding enterprise demo data...")
    seed_database()
    print("✓ Enterprise demo data seeded.")

    # 3. Launch Server
    print("=" * 60)
    print("Starting FastAPI Uvicorn Server on http://localhost:8000 (Docs: http://localhost:8000/docs)...")
    print("=" * 60)

    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
