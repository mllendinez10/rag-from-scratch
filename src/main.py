"""
Run the RAG pipeline by connecting the individual processing steps.

This script will:
- Provide the PDF source
- Load the document pages
- ...

"""

from load_documents import load_documents
from chunk_documents import chunk_documents

# pdf location
pdf_path = "data/ESR-5019.pdf"

# Call function that returns the list with pages 
pages = load_documents(pdf_path)

#Testing the the function load_documents works
print(f"the length of the list of pages is {len(pages)}")

# Call function that returns the list with chunks
chunks = chunk_documents(pages)

#Testing the the function chunk_documents works
print(f"the length of the list of chunks is {len(chunks)}")