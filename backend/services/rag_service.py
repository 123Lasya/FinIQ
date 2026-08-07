from typing import List, Dict, Any
from backend.rag.document_loader import DocumentLoaderService
from backend.rag.vector_store import VectorStoreService
from backend.logging import logger


class RAGService:
    """Service handling policy document ingestion and context search."""

    def __init__(self):
        self.document_loader = DocumentLoaderService()
        self.vector_store = VectorStoreService()

    def ingest_document_file(self, file_path: str, filename: str) -> Dict[str, Any]:
        """Loads, chunks, embeds, and indexes document into ChromaDB."""
        logger.info(f"Ingesting policy document file: {filename}")
        chunks = self.document_loader.process_file(file_path, filename)
        success = self.vector_store.add_documents(chunks)
        return {
            "filename": filename,
            "total_chunks": len(chunks),
            "status": "INGESTED" if success else "FAILED"
        }

    def search_policies(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        return self.vector_store.query(query_text=query, top_k=top_k)
