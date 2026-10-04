import pymupdf
import re
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    Extracts and cleans structured text page-by-page from uploaded PDF files using PyMuPDF.
    Includes text normalization, de-hyphenation, and layout cleanup.
    """

    @staticmethod
    def _clean_text(raw_text: str) -> str:
        """Fixes hyphenated line splits (e.g. 'knowl- edge' -> 'knowledge') and cleans whitespace."""
        if not raw_text:
            return ""
        
        # Join words split by hyphens across lines or spaces
        text = re.sub(r'(\b[a-zA-Z]{2,})-\s*\n\s*([a-zA-Z]{2,}\b)', r'\1\2', raw_text)
        text = re.sub(r'(\b[a-zA-Z]{2,})-\s+([a-zA-Z]{2,}\b)', r'\1\2', text)
        
        # Replace multiple horizontal spaces with single space
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Normalize newline gaps (keep paragraph breaks)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    @staticmethod
    def extract_text_from_bytes(file_bytes: bytes, filename: str = "document.pdf") -> Tuple[str, List[Dict[str, Any]]]:
        """
        Extracts plain text and page metadata from PDF bytes.

        Returns:
            full_text (str): Concatenated text of the entire PDF
            page_data (List[Dict]): List of dicts with {'page': int, 'text': str, 'char_count': int}
        """
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        page_data = []
        full_text_chunks = []

        total_pages = len(doc)
        logger.info(f"Processing PDF '{filename}' with {total_pages} pages.")

        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            raw_text = page.get_text("text").strip()
            cleaned_text = PDFProcessor._clean_text(raw_text)
            
            if cleaned_text:
                page_info = {
                    "page_number": page_num + 1,
                    "text": cleaned_text,
                    "char_count": len(cleaned_text),
                    "filename": filename
                }
                page_data.append(page_info)
                full_text_chunks.append(f"[Page {page_num + 1}]\n{cleaned_text}")

        doc.close()
        full_text = "\n\n".join(full_text_chunks)
        return full_text, page_data

    @staticmethod
    def extract_text_from_path(file_path: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Extract text from a file path on disk."""
        with open(file_path, "rb") as f:
            return PDFProcessor.extract_text_from_bytes(f.read(), filename=file_path.split("/")[-1])

