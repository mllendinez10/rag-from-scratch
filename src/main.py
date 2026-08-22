"""
Run the RAG pipeline by connecting the individual processing steps.

This script will:
- Provide a list with PDFs source paths
- Load and extract the document pages using load_documents.py
- Split the pages into smaller chunks using chunk_documents.py
- Create embeddings and store them in ChromaDB using index_chunks.py 
- Search the best matching chunks using hybrid_search.py

"""

from load_documents import load_documents
from chunk_documents import chunk_documents
from index_chunks import index_chunks
from keyword_search import keyword_search
from semantic_search import semantic_search
from hybrid_search import hybrid_search

# List with PDFs location
pdf_paths = ["data/ESR-5019.pdf", "data/ETA-26:0367.pdf"]

# Load documents
pages = load_documents(pdf_paths)

#Testing the function load_documents works
print(f"the length of the list of pages is {len(pages)}")

# Create chunks
chunks = chunk_documents(pages)

#Testing the function chunk_documents works
print(f"the length of the list of chunks is {len(chunks)}")

# Create embeddings and store them in ChromaDB
index_chunks(chunks)

# User query 
query = "What is the item number for MT-70 0C ?"

# Search the best matching chunks with keyword search BM25
# keyword_results, keyword_scores = keyword_search(query, chunks, top_k=5)
# print(f"keyword result is: {keyword_results}")

# Search the best matching chunks with semantic search
# semantic_result = semantic_search(query, chunks, top_k=5)
# print(f"semantic result is: {semantic_result}")

# Search the best matching chunks with hybrid search
hybrid_result = hybrid_search(query, chunks, top_k=5)
print(f"hybrid result is: {hybrid_result}")