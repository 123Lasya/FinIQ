from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.rag.search_service import SimilaritySearchService
from backend.schemas.document import RetrievalChunkResult
from backend.models.document import KnowledgeDocument
from backend.utils.logger import get_logger

logger = get_logger("finpilot.rag.retrieval")


class KnowledgeRetrievalService:
    """Enterprise Knowledge Retrieval Service delivering top 5 relevant document chunks with metadata and scores."""

    def __init__(self, search_service: SimilaritySearchService = None):
        self.search_service = search_service or SimilaritySearchService()

    def retrieve_relevant_knowledge(
        self,
        query: str,
        db: Session = None,
        top_k: int = 5
    ) -> List[RetrievalChunkResult]:
        """Retrieves top 5 relevant document chunks formatted with similarity scores and document metadata."""
        raw_results = self.search_service.search(query=query, top_k=top_k)
        retrieved_items = []

        for item in raw_results:
            meta = item.get("metadata", {})
            doc_id = meta.get("document_id", "")
            doc_title = meta.get("title", "Enterprise Policy")
            filename = meta.get("filename", "document.pdf")
            category = meta.get("category", "POLICY")
            page_num = meta.get("page_number", 1)

            # If DB session provided, fetch live doc metadata
            if db and doc_id:
                doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.document_id == doc_id).first()
                if doc:
                    doc_title = doc.title
                    filename = doc.filename
                    category = doc.category

            retrieved_items.append(RetrievalChunkResult(
                chunk_id=item.get("chunk_id", ""),
                document_id=doc_id,
                document_title=doc_title,
                filename=filename,
                category=category,
                page_number=page_num,
                chunk_text=item.get("chunk_text", ""),
                similarity_score=item.get("similarity_score", 0.0),
                metadata=meta
            ))

        logger.info(f"KnowledgeRetrievalService retrieved {len(retrieved_items)} top policy context chunks.")
        return retrieved_items

    def retrieve_context_string(self, query: str, db: Session = None, top_k: int = 5) -> str:
        """Formats retrieved chunks into a clean prompt string for AI Agents."""
        chunks = self.retrieve_relevant_knowledge(query, db=db, top_k=top_k)
        if not chunks:
            return "No matching enterprise knowledge base policies found."

        snippets = []
        for idx, c in enumerate(chunks, 1):
            snippets.append(
                f"[Snippet {idx}] Document: {c.document_title} ({c.filename}) | Page: {c.page_number} | Relevance: {c.similarity_score}\n{c.chunk_text}"
            )
        return "\n\n".join(snippets)
