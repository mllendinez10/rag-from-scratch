"""
Load and chunk PDF documents using Docling.

This script will:
- Receive a list of PDF paths
- Convert each PDF into a structured document
- Create structure-aware chunks
- Add document context such as headings to the chunks
- Preserve the source and page metadata
- Return the chunks for keyword and semantic search
"""

from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker


def load_and_chunk_documents_docling(pdf_paths):

    chunks_docling = []
    chunk_number = 1

    # Create the Docling converter and chunker
    converter = DocumentConverter()
    chunker = HybridChunker()

    # Process each PDF
    for pdf_path in pdf_paths:

        # Convert the PDF into a structured document
        document = converter.convert(pdf_path).document

        # Get the PDF filename for metadata
        source = Path(pdf_path).name

        # Create structure-aware chunks
        for chunk in chunker.chunk(dl_doc=document):

            # Add context such as headings to the chunk
            chunk_text = chunker.contextualize(chunk)

            # Page number is unavailable by default
            page_number = None

            # Get the page number from the chunk metadata
            if chunk.meta.doc_items:
                first_item = chunk.meta.doc_items[0]

                if first_item.prov:
                    page_number = first_item.prov[0].page_no

            # Store the chunk using the same structure
            # as the existing RAG pipeline
            chunks_docling.append({
                "chunk": chunk_number,
                "source": source,
                "page": page_number,
                "text": chunk_text
            })

            chunk_number += 1

    return chunks_docling