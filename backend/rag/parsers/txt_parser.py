from typing import List, Dict, Any
from backend.utils.logger import get_logger

logger = get_logger("finpilot.rag.txt")


class TXTParser:
    """Extracts text from plain TXT document files."""

    @staticmethod
    def parse_txt(file_path: str) -> List[Dict[str, Any]]:
        """Parses TXT text files."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            logger.info(f"Parsed TXT file {file_path}.")
            return [{"page_number": 1, "text": content}]
        except Exception as e:
            logger.error(f"Error parsing TXT file {file_path}: {e}")
            return []
