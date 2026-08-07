import os
from typing import List, Dict, Any
from backend.logging import logger


class DocumentLoaderService:
    """Service to load and chunk PDF, DOCX, and TXT compliance policy documents."""

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Splits text into overlapping chunks."""
        if not text:
            return []
        words = text.split()
        chunks = []
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += (chunk_size - overlap)
        return chunks

    def load_txt(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def load_pdf(self, file_path: str) -> str:
        text = ""
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {e}")
        return text

    def load_docx(self, file_path: str) -> str:
        text = ""
        try:
            import docx
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            logger.error(f"Error loading DOCX {file_path}: {e}")
        return text

    def process_file(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Processes file based on extension and returns chunk dictionaries."""
        ext = os.path.splitext(filename)[1].lower()
        content = ""
        if ext == ".txt":
            content = self.load_txt(file_path)
        elif ext == ".pdf":
            content = self.load_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            content = self.load_docx(file_path)
        else:
            logger.warning(f"Unsupported file format extension: {ext}")
            content = self.load_txt(file_path)

        chunks = self.chunk_text(content)
        documents = []
        for idx, chunk in enumerate(chunks):
            documents.append({
                "chunk_id": f"{filename}_chunk_{idx}",
                "content": chunk,
                "metadata": {
                    "source": filename,
                    "chunk_index": idx,
                    "total_chunks": len(chunks)
                }
            })
        return documents
