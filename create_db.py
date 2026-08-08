#!/usr/bin/env python
"""Creates all database tables using SQLAlchemy metadata."""
import sys
import os

# Ensure backend package is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import init_db
from backend.logging import logger

def main():
    logger.info("Initializing database tables for FinPilot AI...")
    try:
        init_db()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
