from typing import List, Dict, Any
from backend.rag.vector_store import VectorStoreService
from backend.logging import logger


class RAGRetrieverService:
    """Service retrieving relevant policies and SOP chunks for AI Agents."""

    def __init__(self, vector_store: VectorStoreService = None):
        self.vector_store = vector_store or VectorStoreService()

    def retrieve_context(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Retrieves top matches for a financial complaint context query."""
        logger.info(f"Retrieving RAG context for query: {query[:60]}...")
        results = self.vector_store.query(query, top_k=top_k)
        return results

    def retrieve_formatted_string(self, query: str, top_k: int = 4) -> str:
        """Retrieves and formats policy context string for LLM prompts."""
        results = self.retrieve_context(query, top_k=top_k)
        if not results:
            return "No matching enterprise policy documents found in knowledge base."

        formatted_snippets = []
        for idx, res in enumerate(results, 1):
            source = res.get("metadata", {}).get("source", "Policy Document")
            formatted_snippets.append(f"--- Policy Snippet {idx} (Source: {source}, Relevance: {res['score']}) ---\n{res['content']}")

        return "\n\n".join(formatted_snippets)
