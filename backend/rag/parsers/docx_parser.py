from typing import List, Dict, Any
from backend.utils.logger import get_logger

logger = get_logger("finpilot.rag.docx")


class DOCXParser:
    """Extracts text from DOCX files using python-docx."""

    @staticmethod
    def parse_docx(file_path: str) -> List[Dict[str, Any]]:
        """Parses DOCX document paragraphs."""
        pages = []
        try:
            import docx
            doc = docx.Document(file_path)
            full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            if full_text:
                pages.append({"page_number": 1, "text": full_text})
            logger.info(f"Parsed DOCX {file_path}: Extracted text payload.")
        except Exception as e:
            logger.error(f"Error parsing DOCX file {file_path}: {e}")
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    pages.append({"page_number": 1, "text": f.read()})
            except Exception as ex:
                logger.error(f"Fallback read failed for DOCX {file_path}: {ex}")
        return pages
