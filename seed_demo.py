#!/usr/bin/env python
"""Seeds demo data into the database."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.demo_data.seed_data import seed_database
from backend.logging import logger

def main():
    logger.info("Executing demo data seeding script...")
    try:
        seed_database()
        print("Demo data seeded successfully! (5 Employees, 20 Customers, 100 Transactions, 30 Investigations, 10 Approvals, 5 Knowledge Documents, 50 Audit Logs, 100 Agent Executions)")
    except Exception as e:
        print(f"Error seeding demo data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
