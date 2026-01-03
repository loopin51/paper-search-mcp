import logging
from typing import List, Dict, Any
from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

logger = logging.getLogger(__name__)

class DoclingProcessor:
    def __init__(self):
        self.converter = DocumentConverter()
        self.chunker = HybridChunker()

    def process_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Convert a PDF file into chunks using Docling.
        Returns a list of dictionaries with 'text' and 'metadata'.
        """
        try:
            # Convert PDF to Docling document
            conversion_result = self.converter.convert(pdf_path)
            doc = conversion_result.document
            
            # Chunk the document
            # HybridChunker returns an iterator of chunks
            chunks = list(self.chunker.chunk(doc))
            
            processed_chunks = []
            for chunk in chunks:
                # Serialize chunk to text and metadata
                # chunk.text contains the text content
                # chunk.meta contains metadata including page numbers, etc.
                metadata = {
                    "source": pdf_path,
                    "page_numbers": [prov.page_no for prov in chunk.prov] if hasattr(chunk, 'prov') else [],
                    # Add other metadata needed
                }
                
                processed_chunks.append({
                    "text": chunk.text,
                    "metadata": metadata
                })
                
            return processed_chunks
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            raise
