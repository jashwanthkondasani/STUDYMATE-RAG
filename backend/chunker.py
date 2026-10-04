from typing import List, Dict, Any
import re
import logging

logger = logging.getLogger(__name__)

class TextChunker:
    """
    Splits long extracted text into semantic overlapping chunks while preserving page number
    and section header metadata. Optimized for high-precision RAG retrieval.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_page_data(self, page_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes extracted page data list and generates overlapping text chunks with precise metadata.
        """
        chunks = []
        global_chunk_idx = 0

        for page in page_data:
            page_text = page["text"]
            page_num = page["page_number"]
            filename = page["filename"]
            
            if not page_text:
                continue

            # Detect section markers on page
            section_tags = []
            if re.search(r'\b(abstract|summary)\b', page_text, re.IGNORECASE):
                section_tags.append("Abstract")
            if re.search(r'\b(keywords?|index terms)\b', page_text, re.IGNORECASE):
                section_tags.append("Keywords")
            if re.search(r'\b(introduction|overview)\b', page_text, re.IGNORECASE):
                section_tags.append("Introduction")
            if re.search(r'\b(conclusion|future work)\b', page_text, re.IGNORECASE):
                section_tags.append("Conclusion")

            section_header = f"[{' | '.join(section_tags)}]" if section_tags else ""

            # Split text into overlapping windows
            start = 0
            text_len = len(page_text)

            while start < text_len:
                end = min(start + self.chunk_size, text_len)
                
                # If not at end, break cleanly at paragraph or sentence boundary
                if end < text_len:
                    last_para = page_text.rfind("\n\n", start + self.chunk_size - 200, end)
                    if last_para != -1 and last_para > start:
                        end = last_para + 2
                    else:
                        last_period = page_text.rfind(".", start + self.chunk_size - 150, end)
                        if last_period != -1 and last_period > start:
                            end = last_period + 1
                        else:
                            last_space = page_text.rfind(" ", start + self.chunk_size - 80, end)
                            if last_space != -1 and last_space > start:
                                end = last_space

                chunk_text = page_text[start:end].strip()

                if len(chunk_text) > 30:  # Ignore tiny noise chunks
                    global_chunk_idx += 1
                    chunk_id = f"{filename}_p{page_num}_c{global_chunk_idx}"
                    
                    # Prepend section metadata if available
                    formatted_text = f"Document: {filename} (Page {page_num}) {section_header}\n{chunk_text}" if section_header else chunk_text

                    chunks.append({
                        "chunk_id": chunk_id,
                        "text": formatted_text,
                        "raw_text": chunk_text,
                        "page_number": page_num,
                        "filename": filename,
                        "section_tags": section_tags,
                        "start_char": start,
                        "end_char": end
                    })

                # Move start pointer forward by (chunk_size - overlap)
                step = self.chunk_size - self.chunk_overlap
                if step <= 0:
                    step = 300
                start += step

        logger.info(f"Generated {len(chunks)} high-precision chunks from {len(page_data)} pages.")
        return chunks

