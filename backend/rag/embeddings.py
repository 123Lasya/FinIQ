import hashlib
from typing import List
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger("finpilot.rag.embeddings")


class EmbeddingService:
    """Generates 384-dimensional dense vector embeddings via SentenceTransformers."""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self._model = None

    def _load_model(self):
        if self._model is not None:
            return self._model

        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading SentenceTransformers embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
        except Exception as e:
            logger.warning(f"SentenceTransformers load warning ({e}). Active fallback embedding engine enabled.")
            self._model = None

        return self._model

    def embed_query(self, text: str) -> List[float]:
        """Embeds single query string."""
        model = self._load_model()
        if model is not None:
            try:
                return model.encode(text, convert_to_numpy=True).tolist()
            except Exception as e:
                logger.error(f"Embedding query error: {e}")

        return self._deterministic_fallback_embedding(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Batch embeds multiple texts."""
        model = self._load_model()
        if model is not None:
            try:
                return model.encode(texts, convert_to_numpy=True).tolist()
            except Exception as e:
                logger.error(f"Batch embedding error: {e}")

        return [self._deterministic_fallback_embedding(t) for t in texts]

    def _deterministic_fallback_embedding(self, text: str) -> List[float]:
        """Generates 384-dim pseudo-random dense vector from text SHA-512 seed."""
        h = hashlib.sha512(text.encode("utf-8")).digest()
        vector = []
        for i in range(384):
            val = (h[i % len(h)] + i * 13) % 256
            norm = (val / 128.0) - 1.0
            vector.append(round(norm, 6))
        return vector
