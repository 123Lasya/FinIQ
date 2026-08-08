#!/usr/bin/env python
"""Launcher script for FinPilot AI FastAPI backend server."""
import sys
import os
import uvicorn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.config import settings

def main():
    print(f"Launching {settings.PROJECT_NAME} backend server on port 8000...")
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
