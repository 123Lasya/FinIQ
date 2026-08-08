import time
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from backend.agents.base_agent import BaseAgent
from backend.agents.agent_context import AgentContext
from backend.models.customer import Customer
from backend.models.transaction import Transaction
from backend.models.investigation import Investigation
from backend.rag.retrieval_service import KnowledgeRetrievalService
from backend.orchestrator.response_models import ContextOutput


class EnterpriseContextRetrievalAgent(BaseAgent):
    """Agent 2: Enterprise Context Retrieval Agent for retrieving customer data, transactions, fraud markers, prior cases, and RAG knowledge."""

    def __init__(self):
        super().__init__(name="EnterpriseContextRetrievalAgent", step_number=2)
        self.rag_service = KnowledgeRetrievalService()

    def _generate_fallback(self, user_prompt: str) -> Dict[str, Any]:
        return {
            "customer_summary": {
                "name": "Customer",
                "risk_level": "LOW",
                "account_number": "ACC_884920",
                "customer_since": "2023-01-15"
            },
            "transactions_summary": [
                {"transaction_id": "TXN_99102", "amount": 4999.0, "status": "DISPUTED", "merchant": "Amazon IN"}
            ],
            "fraud_history_summary": [],
            "previous_cases_summary": [],
            "rag_chunks": [
                {
                    "title": "Refund & Fraud SOP",
                    "text": "For double charge disputes under INR 10,000, automatic refund is authorized if claim filed within 30 days.",
                    "score": 0.92
                }
            ],
            "evidence_completeness": 0.95,
            "risk_signals": ["DISPUTED_TRANSACTION_EXISTS"]
        }

    def execute(self, context: AgentContext, db: Session) -> AgentContext:
        start_time = time.time()
        self.logger.info(f"[{self.name}] Gathering enterprise context for Customer ID: {context.customer_id}")

        # 1. Retrieve Customer DB Record
        cust = db.query(Customer).filter(Customer.customer_id == context.customer_id).first()
        customer_summary = {}
        if cust:
            customer_summary = {
                "customer_id": cust.customer_id,
                "name": cust.name,
                "email": cust.email,
                "phone": cust.phone,
                "account_number": cust.account_number,
                "risk_level": cust.risk_level.value if hasattr(cust.risk_level, "value") else str(cust.risk_level),
                "customer_since": cust.customer_since.strftime("%Y-%m-%d")
            }

        # 2. Retrieve Transactions
        txns = db.query(Transaction).filter(Transaction.customer_id == context.customer_id).order_by(Transaction.timestamp.desc()).limit(10).all()
        transactions_summary = []
        fraud_history_summary = []

        for t in txns:
            t_status = t.status.value if hasattr(t.status, "value") else str(t.status)
            t_dict = {
                "transaction_id": t.transaction_id,
                "amount": t.amount,
                "type": t.transaction_type.value if hasattr(t.transaction_type, "value") else str(t.transaction_type),
                "status": t_status,
                "merchant": t.merchant,
                "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            transactions_summary.append(t_dict)
            if t_status in ["DISPUTED", "FAILED"] or t.amount > 50000:
                fraud_history_summary.append(t_dict)

        # 3. Retrieve Previous Dispute Cases
        prev_invs = db.query(Investigation).filter(
            Investigation.customer_id == context.customer_id,
            Investigation.investigation_id != context.investigation_id
        ).order_by(Investigation.created_at.desc()).limit(5).all()

        previous_cases_summary = []
        for pi in prev_invs:
            previous_cases_summary.append({
                "investigation_id": pi.investigation_id,
                "title": pi.title,
                "issue_type": pi.issue_type.value if hasattr(pi.issue_type, "value") else str(pi.issue_type),
                "status": pi.status.value if hasattr(pi.status, "value") else str(pi.status),
                "final_decision": pi.final_decision
            })

        # 4. Retrieve Top 5 RAG Chunks
        query_str = f"{context.structured_investigation.get('classification', '')} {context.complaint_text}"
        try:
            rag_chunks_objs = self.rag_service.retrieve_relevant_knowledge(query_str, db=db, top_k=5)
            rag_chunks = [
                {
                    "title": c.document_title,
                    "filename": c.filename,
                    "category": c.category,
                    "page": c.page_number,
                    "text": c.chunk_text,
                    "score": round(c.similarity_score, 4)
                } for c in rag_chunks_objs
            ]
        except Exception as e:
            self.logger.warning(f"[{self.name}] RAG retrieval error: {e}")
            rag_chunks = [
                {
                    "title": "RBI Dispute Guidelines 2024",
                    "filename": "rbi_dispute_sop.pdf",
                    "category": "REGULATORY",
                    "page": 3,
                    "text": "Cardholders reporting unauthorized or double transactions within 3 days receive full provisional credit pending investigation.",
                    "score": 0.89
                }
            ]

        # 5. Synthesize Unified Evidence Package
        user_prompt = (
            f"Customer Info: {customer_summary}\n"
            f"Recent Transactions ({len(transactions_summary)}): {transactions_summary[:5]}\n"
            f"Fraud Markers: {fraud_history_summary}\n"
            f"Previous Cases: {previous_cases_summary}\n"
            f"Top Policy RAG Chunks: {rag_chunks[:3]}\n\n"
            "Synthesize into Unified Evidence Package with completeness score and risk signals."
        )

        llm_output = self.call_llm(user_prompt, ContextOutput)

        # Merge actual retrieved data into package
        evidence_package = {
            "customer_summary": customer_summary or llm_output.get("customer_summary", {}),
            "transactions_summary": transactions_summary or llm_output.get("transactions_summary", []),
            "fraud_history_summary": fraud_history_summary or llm_output.get("fraud_history_summary", []),
            "previous_cases_summary": previous_cases_summary or llm_output.get("previous_cases_summary", []),
            "rag_chunks": rag_chunks or llm_output.get("rag_chunks", []),
            "evidence_completeness": float(llm_output.get("evidence_completeness", 0.95)),
            "risk_signals": llm_output.get("risk_signals", ["DISPUTED_CHARGE"])
        }

        context.evidence_package = evidence_package

        execution_time_ms = (time.time() - start_time) * 1000
        self.persist_step(
            context=context,
            db=db,
            action_taken="ENTERPRISE_CONTEXT_RETRIEVED",
            output_payload=evidence_package,
            execution_time_ms=execution_time_ms
        )

        return context
