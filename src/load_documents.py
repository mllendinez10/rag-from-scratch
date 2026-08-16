"""
Load PDF documents and extract their text for use later in the RAG pipeline.

This script will receive a list with PDF paths and:
- Open the PDFs
- Extract the text page by page
- Store the page number and document source as metadata
- Return the extracted pages for the next step: text chunking

"""

from pypdf import PdfReader
from pathlib import Path


def load_documents(pdf_paths):
    
    # Empty list to store extracted pages
    pages = []
    
    # Loop each document
    for pdf_path in pdf_paths:

        # Read PDF
        pdf = PdfReader(pdf_path)
        
        # Document name
        source = Path(pdf_path).name


        # Go through each page of the PDF
        for page_number, page in enumerate(pdf.pages, start=1):

            # Extract text from the page
            text = page.extract_text()

            # Add page number and text to the list
            pages.append({
                "source": source,
                "page": page_number,
                "text": text
                
            })

    return pages