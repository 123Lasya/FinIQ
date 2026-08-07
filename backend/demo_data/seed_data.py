import os
from datetime import datetime
from backend.database import SessionLocal, init_db
from backend.models import User, Transaction, Investigation, PolicyRule
from backend.utils.jwt import get_password_hash
from backend.services.rag_service import RAGService
from backend.logging import logger


def seed_database():
    """Seeds the database and RAG vector store with initial enterprise demo data."""
    logger.info("Starting database seed process...")
    init_db()
    db = SessionLocal()

    try:
        # 1. Seed Default Employee User
        emp = db.query(User).filter(User.employee_id == "EMP-1001").first()
        if not emp:
            emp = User(
                employee_id="EMP-1001",
                email="employee@finpilot.ai",
                hashed_password=get_password_hash("Password123!"),
                full_name="Alex Mercer",
                role="OPERATIONS_EXEC",
                department="Financial Operations",
                is_active=True
            )
            db.add(emp)
            logger.info("Seeded default Employee user: employee@finpilot.ai (EMP-1001)")

        # 2. Seed Policy Rules
        pol1 = db.query(PolicyRule).filter(PolicyRule.policy_code == "POL-REFUND-MAX25K").first()
        if not pol1:
            pol1 = PolicyRule(
                policy_code="POL-REFUND-MAX25K",
                title="Autonomous Refund Ceiling Limit",
                description="Refunds under ₹25,000 can be auto-executed. Claims > ₹25,000 require human officer approval.",
                max_refund_limit=25000.0,
                requires_compliance_review=True,
                is_active=True
            )
            db.add(pol1)

        # 3. Seed Transactions for Customer CUST-9921
        txns = [
            ("TXN-883921", "CUST-9921", 50000.0, "INR", "Reliance Digital Retail", "DEBIT", "SUCCESS"),
            ("TXN-883922", "CUST-9921", 50000.0, "INR", "Reliance Digital Retail", "DEBIT", "SUCCESS"),  # Duplicate entry
            ("TXN-774102", "CUST-4410", 12000.0, "INR", "Swiggy India", "DEBIT", "SUCCESS")
        ]
        for t_id, c_id, amt, curr, merch, t_type, status in txns:
            exists = db.query(Transaction).filter(Transaction.transaction_id == t_id).first()
            if not exists:
                db.add(Transaction(
                    transaction_id=t_id,
                    customer_id=c_id,
                    amount=amt,
                    currency=curr,
                    merchant_name=merch,
                    transaction_type=t_type,
                    status=status
                ))

        # 4. Seed Investigation Tokens (including user request example)
        inv1 = db.query(Investigation).filter(Investigation.token_id == "FIN-2026-88412").first()
        if not inv1:
            inv1 = Investigation(
                token_id="FIN-2026-88412",
                customer_id="CUST-9921",
                customer_name="Rohan Sharma",
                complaint_text="I was charged twice for transaction TXN-883921. Please refund ₹50,000.",
                dispute_amount=50000.0,
                currency="INR",
                priority="HIGH",
                status="PENDING"
            )
            db.add(inv1)

        inv2 = db.query(Investigation).filter(Investigation.token_id == "FIN-2026-11045").first()
        if not inv2:
            inv2 = Investigation(
                token_id="FIN-2026-11045",
                customer_id="CUST-4410",
                customer_name="Priya Patel",
                complaint_text="Swiggy food order failed but amount ₹12,000 was debited. Please refund.",
                dispute_amount=12000.0,
                currency="INR",
                priority="MEDIUM",
                status="PENDING"
            )
            db.add(inv2)

        db.commit()
        logger.info("Database records seeded successfully.")

        # 5. Ingest Sample Policy Document into RAG
        sample_txt_path = os.path.join(os.path.dirname(__file__), "sample_policy.txt")
        if os.path.exists(sample_txt_path):
            rag_service = RAGService()
            rag_service.ingest_document_file(sample_txt_path, "sample_policy.txt")
            logger.info("Ingested sample_policy.txt into RAG vector store.")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
