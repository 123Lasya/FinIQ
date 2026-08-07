import os
import random
from datetime import datetime, timedelta
from backend.database.connection import SessionLocal, init_db
from backend.models import (
    Employee, Customer, Transaction, Investigation,
    KnowledgeDocument, Approval, AuditLog,
    EmployeeRole, CustomerRiskLevel, TransactionType, TransactionStatus,
    InvestigationIssueType, InvestigationPriority, InvestigationStatus,
    ApprovalStatus, ComplianceStatus
)
from backend.utils.security import hash_password
from backend.utils.uuid_utils import generate_uuid, generate_token_id
from backend.services.document_service import DocumentUploadService
from backend.utils.logger import get_logger

logger = get_logger("finpilot.seeder")


def seed_database():
    """Generates realistic demo dataset: 5 Employees, 20 Customers, 100 Transactions, 30 Investigations, 5 Knowledge Docs, 10 Approvals."""
    logger.info("Initializing database schemas for seed population...")
    init_db()
    db = SessionLocal()

    try:
        # Check if seeder has already run
        if db.query(Employee).count() >= 5 and db.query(Customer).count() >= 20:
            logger.info("Database already seeded with enterprise dataset. Skipping seeder.")
            return

        logger.info("Seeding 5 Employees...")
        employees_data = [
            ("Alex Mercer", "alex.mercer@finpilot.ai", EmployeeRole.OPERATIONS_EXEC, "Financial Operations"),
            ("Priya Sharma", "priya.sharma@finpilot.ai", EmployeeRole.CUSTOMER_SUPPORT, "Customer Escalations"),
            ("David Kim", "david.kim@finpilot.ai", EmployeeRole.FRAUD_ANALYST, "Fraud Intelligence"),
            ("Sarah Jenkins", "sarah.jenkins@finpilot.ai", EmployeeRole.COMPLIANCE_OFFICER, "Regulatory Compliance"),
            ("Michael Chen", "michael.chen@finpilot.ai", EmployeeRole.OPERATIONS_EXEC, "Financial Operations"),
        ]

        employees = []
        for name, email, role, dept in employees_data:
            emp = db.query(Employee).filter(Employee.email == email).first()
            if not emp:
                emp = Employee(
                    name=name,
                    email=email,
                    password_hash=hash_password("Password123!"),
                    department=dept,
                    role=role
                )
                db.add(emp)
                db.flush()
            employees.append(emp)

        db.commit()

        logger.info("Seeding 20 Customers...")
        customers = []
        for i in range(1, 21):
            email = f"customer{i}@bank.com"
            cust = db.query(Customer).filter(Customer.email == email).first()
            if not cust:
                risk = random.choice([CustomerRiskLevel.LOW, CustomerRiskLevel.LOW, CustomerRiskLevel.MEDIUM, CustomerRiskLevel.HIGH])
                if i == 5:
                    risk = CustomerRiskLevel.CRITICAL
                cust = Customer(
                    name=f"Customer {i} User",
                    email=email,
                    phone=f"+91-98765{i:05d}",
                    account_number=f"ACC-994021{i:04d}",
                    risk_level=risk,
                    customer_since=datetime.utcnow() - timedelta(days=random.randint(100, 1000))
                )
                db.add(cust)
                db.flush()
            customers.append(cust)

        db.commit()

        logger.info("Seeding 100 Financial Transactions...")
        txns_count = db.query(Transaction).count()
        if txns_count < 100:
            merchants = ["Amazon India", "Flipkart Retail", "Reliance Digital", "Swiggy", "Uber Rides", "Apple Store", "Zomato", "MakeMyTrip", "D Mart", "Starbucks"]
            payment_methods = ["CREDIT_CARD", "DEBIT_CARD", "UPI", "NET_BANKING"]

            # Specific double charge pair for Customer 1
            t1 = Transaction(
                transaction_id="TXN-883921",
                customer_id=customers[0].customer_id,
                amount=50000.0,
                transaction_type=TransactionType.DEBIT,
                status=TransactionStatus.SUCCESS,
                merchant="Reliance Digital",
                payment_method="CREDIT_CARD",
                timestamp=datetime.utcnow() - timedelta(hours=5)
            )
            t2 = Transaction(
                transaction_id="TXN-883922",
                customer_id=customers[0].customer_id,
                amount=50000.0,
                transaction_type=TransactionType.DEBIT,
                status=TransactionStatus.SUCCESS,
                merchant="Reliance Digital",
                payment_method="CREDIT_CARD",
                timestamp=datetime.utcnow() - timedelta(hours=5)
            )
            db.add_all([t1, t2])

            for k in range(3, 101):
                cust = random.choice(customers)
                amt = round(random.uniform(500, 75000), 2)
                t_type = random.choice([TransactionType.DEBIT, TransactionType.DEBIT, TransactionType.DEBIT, TransactionType.CREDIT])
                status = random.choice([TransactionStatus.SUCCESS, TransactionStatus.SUCCESS, TransactionStatus.SUCCESS, TransactionStatus.PENDING, TransactionStatus.FAILED])
                t = Transaction(
                    transaction_id=f"TXN-{100000 + k}",
                    customer_id=cust.customer_id,
                    amount=amt,
                    transaction_type=t_type,
                    status=status,
                    merchant=random.choice(merchants),
                    payment_method=random.choice(payment_methods),
                    timestamp=datetime.utcnow() - timedelta(days=random.randint(1, 60), hours=random.randint(1, 23))
                )
                db.add(t)

            db.commit()

        logger.info("Seeding 30 Investigations & 10 Approval Cases...")
        inv_count = db.query(Investigation).count()
        if inv_count < 30:
            issue_types = list(InvestigationIssueType)
            priorities = list(InvestigationPriority)
            statuses = [
                InvestigationStatus.PENDING,
                InvestigationStatus.IN_PROGRESS,
                InvestigationStatus.AUTO_EXECUTED,
                InvestigationStatus.REQUIRES_HUMAN_APPROVAL,
                InvestigationStatus.APPROVED,
                InvestigationStatus.REJECTED
            ]

            # Primary Example Case: ₹50,000 double charge for Customer 1
            main_inv = Investigation(
                token_id="FIN-2026-88412",
                customer_id=customers[0].customer_id,
                title="Double Charge Claim ₹50,000",
                description="I was charged twice for transaction TXN-883921. Please refund ₹50,000 immediately.",
                issue_type=InvestigationIssueType.DOUBLE_CHARGE,
                priority=InvestigationPriority.HIGH,
                status=InvestigationStatus.REQUIRES_HUMAN_APPROVAL,
                current_agent="PolicyGuardrailAgent",
                decision_type="HUMAN_APPROVAL_REQUIRED",
                final_decision="Pending Human Review (Exceeds ₹25,000 Threshold)",
                created_by=employees[0].employee_id
            )
            db.add(main_inv)
            db.flush()

            investigations = [main_inv]

            for idx in range(2, 31):
                cust = random.choice(customers)
                creator = random.choice(employees)
                i_type = random.choice(issue_types)
                prio = random.choice(priorities)
                st = random.choice(statuses)

                inv = Investigation(
                    token_id=f"FIN-2026-{10000 + idx}",
                    customer_id=cust.customer_id,
                    title=f"{i_type.value.replace('_', ' ').title()} - {cust.name}",
                    description=f"Customer dispute regarding {i_type.value}. Amount requested: ₹{random.randint(1000, 60000)}.",
                    issue_type=i_type,
                    priority=prio,
                    status=st,
                    created_by=creator.employee_id
                )
                db.add(inv)
                db.flush()
                investigations.append(inv)

            db.commit()

            # Seed 10 Human Approvals
            logger.info("Seeding 10 Human Approval Cases...")
            for idx in range(10):
                inv_target = investigations[idx]
                app_status = random.choice([ApprovalStatus.PENDING, ApprovalStatus.APPROVED, ApprovalStatus.REJECTED])
                rev = random.choice(employees)
                approval = Approval(
                    investigation_id=inv_target.investigation_id,
                    reviewed_by=rev.employee_id,
                    status=app_status,
                    reason=f"Reviewed investigation token {inv_target.token_id}. Compliance checks validated.",
                    reviewed_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
                )
                db.add(approval)

            db.commit()

        logger.info("Seeding 5 Knowledge Base Documents...")
        doc_service = DocumentUploadService()
        demo_docs = [
            ("Refund Policy.pdf", "Standard Customer Refund Operating Policy", "REFUND_POLICY"),
            ("RBI Guidelines.pdf", "RBI Regulatory Framework on Financial Disputes", "REGULATORY"),
            ("Fraud Detection SOP.pdf", "Standard Operating Procedure for Fraud Detection", "FRAUD_SOP"),
            ("Internal Operations Manual.pdf", "Internal Operations & Execution Playbook", "OPERATIONS_MANUAL"),
            ("Compliance Policy.pdf", "Enterprise Zero-Trust Compliance Policy", "COMPLIANCE_POLICY"),
        ]

        docs_dir = os.path.join(os.path.dirname(__file__), "demo_docs")
        os.makedirs(docs_dir, exist_ok=True)

        for filename, title, category in demo_docs:
            existing = db.query(KnowledgeDocument).filter(KnowledgeDocument.filename == filename).first()
            if not existing:
                file_path = os.path.join(docs_dir, filename)

                # Generate clean sample text file for indexing
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"""
=== ENTERPRISE DOCUMENT: {title} ({filename}) ===
Category: {category}

1. POLICY STATEMENT
This enterprise document defines regulatory and operational requirements for handling dispute cases in financial operations.

2. DISPUTE REFUND BOUNDARIES
- Autonomous Execution Ceiling: Single refund claims equal to or under ₹25,000 INR may be automatically processed by the AI Execution Agent if Zero Trust verification passes.
- Mandatory Human Officer Approval: Refund claims exceeding ₹25,000 INR (such as ₹50,000 INR double charge claims) CANNOT be auto-executed and mandate review by a human Operations Executive.

3. PRIVACY & SECURITY
Zero Knowledge Privacy Engine must redact PII (PAN, SSN, Credit Card numbers, CVV, passwords) before AI processing.
""")

                doc_service.process_and_index_document(
                    db=db,
                    file_path=file_path,
                    title=title,
                    filename=filename,
                    category=category,
                    uploaded_by_employee_id=employees[0].employee_id
                )

        logger.info("Seeder successfully finished! Enterprise dataset populated cleanly.")

    except Exception as e:
        logger.error(f"Seeder failed with error: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
