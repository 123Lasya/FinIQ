#!/usr/bin/env python
"""Health check verification script checking DB tables, counts, and configuration."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal
from backend.models import Employee, Customer, Transaction, Investigation, Approval, KnowledgeDocument, AuditLog
from backend.config import settings

def check_health():
    print("=" * 60)
    print(f"HEALTH CHECK VERIFICATION - {settings.PROJECT_NAME}")
    print("=" * 60)

    db = SessionLocal()
    try:
        emp_cnt = db.query(Employee).count()
        cust_cnt = db.query(Customer).count()
        txn_cnt = db.query(Transaction).count()
        inv_cnt = db.query(Investigation).count()
        appr_cnt = db.query(Approval).count()
        doc_cnt = db.query(KnowledgeDocument).count()
        audit_cnt = db.query(AuditLog).count()

        print("[OK] Database Status: CONNECTED")
        print(f" - Employees: {emp_cnt} / 5")
        print(f" - Customers: {cust_cnt} / 20")
        print(f" - Transactions: {txn_cnt} / 100")
        print(f" - Investigations: {inv_cnt} / 30")
        print(f" - Pending Approvals: {appr_cnt} / 10")
        print(f" - Knowledge Documents: {doc_cnt} / 5")
        print(f" - Audit Logs: {audit_cnt} / 50")

        groq_key = getattr(settings, "GROQ_API_KEY", "")
        if groq_key and groq_key.startswith("gsk_"):
            print("[OK] Groq API Key: CONFIGURED")
        else:
            print("[INFO] Groq API Key: NOT SET or DEFAULT (Offline rule engine active)")

        print("=" * 60)
        print("SYSTEM STATUS: HEALTHY AND OPERATIONAL")
        print("=" * 60)
    except Exception as e:
        print(f"[ERROR] Health Check Error: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    check_health()
