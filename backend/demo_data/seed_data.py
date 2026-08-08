import os
import random
import uuid
import json
import hashlib
from datetime import datetime, timedelta
from backend.database import SessionLocal, init_db
from backend.models import (
    Employee,
    Customer,
    Transaction,
    Investigation,
    Approval,
    AuditLog,
    KnowledgeDocument,
    AgentExecutionLog,
    AgentArtifact
)
from backend.models.enums import (
    EmployeeRole,
    CustomerRiskLevel,
    TransactionType,
    TransactionStatus,
    InvestigationIssueType,
    InvestigationPriority,
    InvestigationStatus,
    ApprovalStatus,
    ComplianceStatus,
    EmbeddingStatus,
    AgentExecutionStatus
)
from backend.utils.jwt import get_password_hash
from backend.utils.uuid_utils import generate_uuid, generate_token_id
from backend.logging import logger


def seed_database():
    """Seeds database with complete enterprise demo data:
    5 Employees, 20 Customers, 100 Transactions, 30 Investigations,
    10 Pending Approvals, 5 Knowledge Documents, 50 Audit Logs, 100 Agent Executions.
    """
    logger.info("Starting complete enterprise database seed process...")
    init_db()
    db = SessionLocal()

    try:
        # 1. Seed 5 Employees
        employee_configs = [
            ("EMP-1001", "Alex Mercer", "employee@finpilot.ai", EmployeeRole.OPERATIONS_EXEC, "Financial Operations"),
            ("EMP-1002", "Sarah Jenkins", "sarah.j@finpilot.ai", EmployeeRole.CUSTOMER_SUPPORT, "Customer Support"),
            ("EMP-1003", "David Chen", "david.c@finpilot.ai", EmployeeRole.FRAUD_ANALYST, "Fraud Risk Ops"),
            ("EMP-1004", "Maria Rodriguez", "maria.r@finpilot.ai", EmployeeRole.COMPLIANCE_OFFICER, "Regulatory Compliance"),
            ("EMP-1005", "Michael Vance", "michael.v@finpilot.ai", EmployeeRole.OPERATIONS_EXEC, "Operations Management"),
        ]

        employees = []
        for emp_id, name, email, role, dept in employee_configs:
            emp = db.query(Employee).filter(Employee.email == email).first()
            if not emp:
                emp = Employee(
                    employee_id=emp_id,
                    name=name,
                    email=email,
                    password_hash=get_password_hash("Password123!"),
                    role=role,
                    department=dept
                )
                db.add(emp)
                db.flush()
            employees.append(emp)

        db.commit()

        # 2. Seed 20 Customers
        customers = []
        customer_names = [
            "Rohan Sharma", "Priya Patel", "Amitabh Verma", "Sneha Gupta", "Vikram Singh",
            "Ananya Iyer", "Rajesh Kumar", "Meera Nair", "Sanjay Reddy", "Pooja Banerjee",
            "Karan Malhotra", "Divya Joshi", "Arjun Kapoor", "Kavita Rao", "Nikhil Saxena",
            "Shweta Mishra", "Tarun Choudhury", "Ritu Deshmukh", "Gaurav Bhatt", "Neha Kulkarni"
        ]

        for idx, c_name in enumerate(customer_names, 1):
            c_email = f"customer{idx}@example.com"
            c_acct = f"ACC_88{1000 + idx}"
            cust = db.query(Customer).filter(Customer.email == c_email).first()
            if not cust:
                risk = CustomerRiskLevel.CRITICAL if idx in [3, 7] else (CustomerRiskLevel.HIGH if idx in [5, 12] else CustomerRiskLevel.LOW)
                cust = Customer(
                    customer_id=f"CUST-{9900 + idx}",
                    name=c_name,
                    email=c_email,
                    phone=f"+9198765{10000 + idx}",
                    account_number=c_acct,
                    risk_level=risk,
                    customer_since=datetime.utcnow() - timedelta(days=idx * 30)
                )
                db.add(cust)
                db.flush()
            customers.append(cust)

        db.commit()

        # 3. Seed 100 Transactions
        merchants = ["Amazon IN", "Reliance Digital", "Swiggy", "Zomato", "Flipkart", "MakeMyTrip", "Uber", "BookMyShow", "Tata CLiQ", "Croma"]
        transactions = []
        for cust in customers:
            for t_idx in range(5):
                t_id = f"TXN-{cust.customer_id[-4:]}-{t_idx + 101}"
                txn = db.query(Transaction).filter(Transaction.transaction_id == t_id).first()
                if not txn:
                    amt = random.choice([4999.0, 12000.0, 2500.0, 50000.0, 850.0, 15000.0, 3200.0])
                    t_status = TransactionStatus.DISPUTED if t_idx == 0 and cust.risk_level in [CustomerRiskLevel.HIGH, CustomerRiskLevel.CRITICAL] else TransactionStatus.SUCCESS
                    txn = Transaction(
                        transaction_id=t_id,
                        customer_id=cust.customer_id,
                        amount=amt,
                        transaction_type=TransactionType.DEBIT,
                        status=t_status,
                        merchant=random.choice(merchants),
                        payment_method="CREDIT_CARD",
                        timestamp=datetime.utcnow() - timedelta(days=t_idx * 2, hours=t_idx * 3)
                    )
                    db.add(txn)
                    db.flush()
                transactions.append(txn)

        db.commit()

        # 4. Seed 30 Investigations
        investigation_samples = [
            ("FIN-2026-88412", "Double Debit Charge Dispute", "I was charged twice for transaction TXN-9901-101. Please refund ₹50,000.", InvestigationIssueType.DOUBLE_CHARGE, InvestigationPriority.HIGH, InvestigationStatus.PENDING, 50000.0),
            ("FIN-2026-11045", "Failed Swiggy Food Order Reversal", "Swiggy food order failed but amount ₹12,000 was debited.", InvestigationIssueType.FAILED_TRANSFER, InvestigationPriority.MEDIUM, InvestigationStatus.PENDING, 12000.0),
            ("FIN-2026-99102", "Unauthorized Card Transaction", "Stolen card used at electronics store for ₹49,999.", InvestigationIssueType.UNAUTHORIZED_TRANSACTION, InvestigationPriority.CRITICAL, InvestigationStatus.REQUIRES_HUMAN_APPROVAL, 49999.0),
            ("FIN-2026-33419", "Annual Service Fee Dispute", "Disputing annual maintenance fee debit of ₹1,500.", InvestigationIssueType.FEE_DISPUTE, InvestigationPriority.LOW, InvestigationStatus.AUTO_EXECUTED, 1500.0),
        ]

        # Expand to 30 investigations
        investigations = []
        for i in range(1, 31):
            if i <= len(investigation_samples):
                tok_id, title, desc_text, issue_type, priority, status, amt = investigation_samples[i - 1]
            else:
                tok_id = f"FIN-2026-{70000 + i}"
                title = f"Customer Dispute Claim #{i}"
                desc_text = f"Dispute regarding recent card transaction #{i} debit."
                issue_type = random.choice(list(InvestigationIssueType))
                priority = random.choice(list(InvestigationPriority))
                status = random.choice([InvestigationStatus.PENDING, InvestigationStatus.AUTO_EXECUTED, InvestigationStatus.REQUIRES_HUMAN_APPROVAL, InvestigationStatus.APPROVED])
                amt = float(random.randint(500, 45000))

            inv = db.query(Investigation).filter(Investigation.token_id == tok_id).first()
            if not inv:
                cust_choice = customers[(i - 1) % len(customers)]
                inv = Investigation(
                    investigation_id=generate_uuid(),
                    token_id=tok_id,
                    customer_id=cust_choice.customer_id,
                    title=title,
                    description=desc_text,
                    issue_type=issue_type,
                    priority=priority,
                    status=status,
                    current_agent="AuditAgent" if status != InvestigationStatus.PENDING else "IntelligentCaseIntakeAgent",
                    final_decision="FULL_REFUND" if status in [InvestigationStatus.AUTO_EXECUTED, InvestigationStatus.APPROVED] else None,
                    decision_type="PROVISIONAL_CREDIT",
                    created_by=employees[0].employee_id,
                    completed_at=datetime.utcnow() if status != InvestigationStatus.PENDING else None
                )
                db.add(inv)
                db.flush()
            investigations.append(inv)

        db.commit()

        # 5. Seed 10 Pending Approvals
        approvals = []
        requires_approval_invs = [inv for inv in investigations if inv.status == InvestigationStatus.REQUIRES_HUMAN_APPROVAL]
        for idx, inv in enumerate(requires_approval_invs[:10]):
            appr = db.query(Approval).filter(Approval.investigation_id == inv.investigation_id).first()
            if not appr:
                appr = Approval(
                    approval_id=generate_uuid(),
                    investigation_id=inv.investigation_id,
                    reviewed_by=employees[0].employee_id,
                    status=ApprovalStatus.PENDING,
                    reason=f"High value transaction ({inv.title}) requires human authorization under Policy SOP.",
                    reviewed_at=datetime.utcnow()
                )
                db.add(appr)
                db.flush()
            approvals.append(appr)

        db.commit()

        # 6. Seed 5 Knowledge Documents
        kd_titles = [
            ("RBI Customer Protection Circular 2024", "rbi_dispute_sop.pdf", "REGULATORY"),
            ("Enterprise Refund & Credit SOP", "refund_policy_sop.docx", "POLICY"),
            ("Fraud Risk Operations Handbook", "fraud_risk_handbook.pdf", "FRAUD_SOP"),
            ("Core Banking Dispute Resolution Framework", "banking_dispute_framework.txt", "OPERATIONS"),
            ("Merchant Chargeback SOP", "chargeback_rules.pdf", "POLICY")
        ]

        for title, filename, cat in kd_titles:
            doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.filename == filename).first()
            if not doc:
                doc = KnowledgeDocument(
                    document_id=generate_uuid(),
                    title=title,
                    filename=filename,
                    category=cat,
                    file_path=os.path.join(os.getcwd(), "uploads", filename),
                    chunk_count=12,
                    embedding_status=EmbeddingStatus.COMPLETED,
                    uploaded_by=employees[0].employee_id
                )
                db.add(doc)

        db.commit()

        # 7. Seed 100 Agent Execution Logs & Artifacts across completed investigations
        agent_names = [
            "IntelligentCaseIntakeAgent", "EnterpriseContextRetrievalAgent", "DecisionIntelligenceAgent",
            "ZeroTrustDecisionValidationAgent", "PreFlightShadowSimulationAgent", "ZeroKnowledgePrivacyEngine",
            "PolicyGuardrailAgent", "ExecutionAgent", "AuditAgent"
        ]

        for inv in investigations:
            if inv.status != InvestigationStatus.PENDING:
                for step_idx, a_name in enumerate(agent_names, 1):
                    exec_log = AgentExecutionLog(
                        execution_id=generate_uuid(),
                        investigation_id=inv.investigation_id,
                        agent_name=a_name,
                        status=AgentExecutionStatus.SUCCESS,
                        execution_time=round(random.uniform(0.1, 0.4), 3),
                        confidence=round(random.uniform(0.88, 0.98), 2),
                        model_used="llama-3.3-70b-versatile",
                        started_at=inv.created_at + timedelta(seconds=step_idx),
                        completed_at=inv.created_at + timedelta(seconds=step_idx + 1)
                    )
                    db.add(exec_log)

                    artifact = AgentArtifact(
                        artifact_id=generate_uuid(),
                        investigation_id=inv.investigation_id,
                        agent_name=a_name,
                        artifact_type=f"{a_name}_output",
                        artifact_json=json.dumps({"status": "SUCCESS", "step": step_idx, "agent": a_name})
                    )
                    db.add(artifact)

        db.commit()

        # 8. Seed 50 Audit Logs
        for inv in investigations[:50] if len(investigations) >= 50 else investigations:
            audit = db.query(AuditLog).filter(AuditLog.investigation_id == inv.investigation_id).first()
            if not audit:
                raw_hash = f"{inv.investigation_id}:{inv.token_id}:{datetime.utcnow().timestamp()}"
                audit_hash = hashlib.sha256(raw_hash.encode("utf-8")).hexdigest()
                audit = AuditLog(
                    audit_id=generate_uuid(),
                    investigation_id=inv.investigation_id,
                    audit_hash=audit_hash,
                    decision_type=inv.final_decision or "FULL_REFUND",
                    compliance_status=ComplianceStatus.PASSED,
                    remarks=f"Immutable audit trail verified for token {inv.token_id}."
                )
                db.add(audit)

        db.commit()
        logger.info("Successfully seeded complete enterprise demo database (Employees, Customers, Txns, Investigations, Approvals, Knowledge, Audits).")

    except Exception as e:
        logger.error(f"Error seeding database: {e}", exc_info=True)
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
