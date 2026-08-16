"""
Run the RAG pipeline by connecting the individual processing steps.

This script will:
- Provide a list with PDFs source paths
- Load and extract the document pages using load_documents.py
- Split the pages into smaller chunks using chunk_documents.py

"""

from load_documents import load_documents
from chunk_documents import chunk_documents

# pdf location
pdf_paths = ["data/ESR-5019.pdf", "data/ETA-26:0367.pdf"]

# Call function that returns the list with pages 
pages = load_documents(pdf_paths)

#Testing the the function load_documents works
print(f"the length of the list of pages is {len(pages)}")
print(f"This is an example of how a page looks like: {pages[0]}")

# Call function that returns the list with chunks
chunks = chunk_documents(pages)

#Testing the the function chunk_documents works
print(f"the length of the list of chunks is {len(chunks)}")
print(f"This is an example of how a chunk looks like: {chunks[0]}")