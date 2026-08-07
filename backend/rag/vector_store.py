import os
from typing import List, Dict, Any, Optional
from backend.config import settings
from backend.utils.logger import get_logger
from backend.rag.embeddings import EmbeddingService

logger = get_logger("finpilot.rag.vector_store")


class VectorStoreService:
    """Manages ChromaDB vector store collection for policy and guideline documents."""

    def __init__(self):
        self.persist_dir = settings.CHROMA_PERSIST_DIR
        self.embedding_service = EmbeddingService()
        self.client = None
        self.collection = None
        self._memory_store: List[Dict[str, Any]] = []
        self._init_chroma()

    def _init_chroma(self):
        try:
            import chromadb
            os.makedirs(self.persist_dir, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_dir)
            self.collection = self.client.get_or_create_collection(
                name="finpilot_knowledge_base",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("ChromaDB vector store collection initialized.")
        except Exception as e:
            logger.warning(f"ChromaDB persistent client init warning ({e}). Running in-memory vector store mode.")
            self.client = None
            self.collection = None

    def upsert_chunks(self, chunks: List[Dict[str, Any]], metadatas: List[Dict[str, Any]]) -> List[str]:
        """Inserts chunk embeddings and metadata into ChromaDB vector store."""
        if not chunks:
            return []

        ids = [c["chunk_id"] for c in chunks]
        texts = [c["chunk_text"] for c in chunks]
        embeddings = self.embedding_service.embed_documents(texts)

        if self.collection is not None:
            try:
                self.collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=metadatas
                )
                logger.info(f"Upserted {len(chunks)} chunks into ChromaDB collection.")
                return ids
            except Exception as e:
                logger.error(f"ChromaDB upsert error: {e}")

        # Fallback memory store
        for i, chunk in enumerate(chunks):
            self._memory_store.append({
                "id": ids[i],
                "text": texts[i],
                "metadata": metadatas[i],
                "embedding": embeddings[i]
            })
        logger.info(f"Upserted {len(chunks)} chunks into fallback memory vector store.")
        return ids

    def search_similar(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Queries ChromaDB or fallback store and returns top K matches with similarity scores."""
        query_embedding = self.embedding_service.embed_query(query_text)

        if self.collection is not None:
            try:
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k
                )
                formatted = []
                if results and "documents" in results and results["documents"]:
                    docs = results["documents"][0]
                    metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
                    ids = results["ids"][0] if "ids" in results else [""] * len(docs)
                    distances = results["distances"][0] if "distances" in results and results["distances"] else [0.0] * len(docs)

                    for idx in range(len(docs)):
                        dist = float(distances[idx]) if distances else 0.1
                        score = round(max(0.0, min(1.0, 1.0 - dist)), 4)
                        formatted.append({
                            "chunk_id": ids[idx],
                            "chunk_text": docs[idx],
                            "metadata": metas[idx],
                            "similarity_score": score
                        })
                return formatted
            except Exception as e:
                logger.error(f"ChromaDB search failed ({e}). Falling back to memory similarity search.")

        # In-memory cosine similarity calculation
        results = []
        for item in self._memory_store:
            score = self._cosine_sim(query_embedding, item["embedding"])
            results.append({
                "chunk_id": item["id"],
                "chunk_text": item["text"],
                "metadata": item["metadata"],
                "similarity_score": round(score, 4)
            })
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]

    def _cosine_sim(self, v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        n1 = sum(a * a for a in v1) ** 0.5
        n2 = sum(b * b for b in v2) ** 0.5
        return (dot / (n1 * n2)) if n1 > 0 and n2 > 0 else 0.0
