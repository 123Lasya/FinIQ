import sys
from types import SimpleNamespace

from backend.rag.embeddings import EmbeddingService


def test_embedding_service_defers_model_loading_until_use(monkeypatch):
    calls = []

    class FakeSentenceTransformer:
        def __init__(self, model_name):
            calls.append(model_name)
            raise RuntimeError("load failed")

    monkeypatch.setitem(
        sys.modules,
        "sentence_transformers",
        SimpleNamespace(SentenceTransformer=FakeSentenceTransformer),
    )

    service = EmbeddingService(model_name="test-model")

    assert calls == []

    result = service.embed_query("hello")

    assert result == service._deterministic_fallback_embedding("hello")
    assert calls == ["test-model"]
