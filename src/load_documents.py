"""
Load a PDF document and extract its text so it can be used later in the RAG pipeline.

This script will receive a PDF file path and:
- Open the PDF
- Extract the text page by page
- Store the page number as metadata
- Return the extracted pages for the next step: text chunking
"""

from pypdf import PdfReader


def load_documents(pdf_path):

    # Open PDF
    pdf = PdfReader(pdf_path)

    # Empty list to store extracted pages
    pages = []

    # Go through each page of the PDF
    for page_number, page in enumerate(pdf.pages, start=1):

        # Extract text from the page
        text = page.extract_text()

        # Add page number and text to the list
        pages.append({
            "page": page_number,
            "text": text
        })

    return pages