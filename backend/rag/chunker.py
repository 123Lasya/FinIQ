from typing import List, Dict, Any
from backend.utils.logger import get_logger

logger = get_logger("finpilot.rag.chunker")


class ChunkingService:
    """Splits raw document pages into overlapping text chunks for vector indexing."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_pages(self, pages: List[Dict[str, Any]], document_id: str) -> List[Dict[str, Any]]:
        """Splits page text records into structured document chunks."""
        chunks = []
        global_index = 0

        for page in pages:
            page_num = page.get("page_number", 1)
            text = page.get("text", "")
            words = text.split()

            if not words:
                continue

            i = 0
            while i < len(words):
                chunk_words = words[i:i + self.chunk_size]
                chunk_text = " ".join(chunk_words)

                chunks.append({
                    "chunk_index": global_index,
                    "document_id": document_id,
                    "page_number": page_num,
                    "chunk_text": chunk_text
                })
                global_index += 1
                i += (self.chunk_size - self.chunk_overlap)

        logger.info(f"ChunkingService created {len(chunks)} text chunks for document_id '{document_id}'.")
        return chunks
