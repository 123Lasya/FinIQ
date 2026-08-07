from typing import List, Dict, Any
from backend.utils.logger import get_logger

logger = get_logger("finpilot.rag.pdf")


class PDFParser:
    """Extracts text from PDF document files using PyPDF."""

    @staticmethod
    def parse_pdf(file_path: str) -> List[Dict[str, Any]]:
        """Parses PDF page by page and returns list of page dicts."""
        pages = []
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            for i, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append({"page_number": i, "text": text})
            logger.info(f"Parsed PDF {file_path}: Extracted {len(pages)} pages.")
        except Exception as e:
            logger.error(f"Error parsing PDF file {file_path}: {e}")
            # Fallback plain text read if PDF reader encounters unhandled formatting
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    pages.append({"page_number": 1, "text": f.read()})
            except Exception as ex:
                logger.error(f"Fallback text read failed for PDF {file_path}: {ex}")
        return pages
