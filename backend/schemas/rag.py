from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class DocumentIngestRequest(BaseModel):
    title: str
    category: str = "FINANCIAL_POLICY"


class SearchQuery(BaseModel):
    query: str
    top_k: int = 4


class SearchResult(BaseModel):
    document_id: str
    content: str
    metadata: Dict[str, Any]
    score: float
