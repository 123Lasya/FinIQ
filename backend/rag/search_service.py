from typing import List, Dict, Any
from backend.rag.vector_store import VectorStoreService
from backend.utils.logger import get_logger

logger = get_logger("finpilot.rag.search")


class SimilaritySearchService:
    """Service executing similarity vector search over the knowledge collection."""

    def __init__(self, vector_store: VectorStoreService = None):
        self.vector_store = vector_store or VectorStoreService()

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Performs cosine similarity search for query against indexed document chunks."""
        logger.info(f"Performing similarity search for query: '{query[:60]}...' (Top {top_k})")
        return self.vector_store.search_similar(query_text=query, top_k=top_k)
