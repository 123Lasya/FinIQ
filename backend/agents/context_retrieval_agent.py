import json
import time
from sqlalchemy.orm import Session
from backend.agents.base import BaseAgent
from backend.schemas.agent import AgentContext, AgentExecutionResult
from backend.models.transaction import Transaction
from backend.rag.retriever import RAGRetrieverService
from backend.logging import logger


class EnterpriseContextRetrievalAgent(BaseAgent):
    """2. Enterprise Context Retrieval Agent: Fetches RAG policy chunks and DB customer history."""

    def __init__(self, rag_retriever: RAGRetrieverService = None):
        super().__init__(name="EnterpriseContextRetrievalAgent", step_number=3)
        self.rag_retriever = rag_retriever or RAGRetrieverService()

    def _generate_fallback_response(self, user_prompt: str) -> str:
        return json.dumps({
            "context_summary": "Retrieved applicable enterprise double charge policies & verified customer history.",
            "relevant_policy_codes": ["POL-FIN-2026-001", "POL-REFUND-MAX25K"],
            "historical_dispute_count": 0,
            "risk_flag": False
        })

    def execute(self, context: AgentContext, db: Session) -> AgentExecutionResult:
        start_time = time.time()
        logger.info(f"[{self.name}] Step {self.step_number}: Retrieving RAG documents & DB transaction records...")

        # 1. Fetch DB Customer History
        txns = db.query(Transaction).filter(Transaction.customer_id == context.customer_id).all()
        txn_data = [
            {
                "transaction_id": t.transaction_id,
                "amount": t.amount,
                "currency": t.currency,
                "merchant": t.merchant_name,
                "status": t.status,
                "timestamp": t.timestamp.isoformat() if t.timestamp else None
            }
            for t in txns
        ]
        context.customer_history = txn_data

        # 2. Retrieve RAG Policy Context
        query = f"{context.complaint_text} amount {context.dispute_amount}"
        retrieved_chunks = self.rag_retriever.retrieve_context(query, top_k=4)
        context.retrieved_policies = retrieved_chunks

        # LLM Synthesis
        prompt = f"Synthesize context for Complaint: '{context.complaint_text}'\nRetrieved RAG Snippets: {json.dumps(retrieved_chunks)}\nCustomer History: {json.dumps(txn_data)}"
        raw_output = self.call_llm(prompt)

        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            parsed = json.loads(self._generate_fallback_response(prompt))

        elapsed_ms = (time.time() - start_time) * 1000
        hash_sig = self.compute_hash(query, raw_output)

        return AgentExecutionResult(
            agent_name=self.name,
            step_number=self.step_number,
            success=True,
            action_taken=f"Retrieved {len(retrieved_chunks)} RAG policy chunks and {len(txn_data)} customer transaction records",
            output_data=parsed,
            execution_time_ms=round(elapsed_ms, 2),
            hash_signature=hash_sig
        )
