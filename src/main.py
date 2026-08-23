"""
Run the RAG pipeline by connecting the individual processing steps.

This script will:
- Provide a list with PDFs source paths
- Load and extract the document pages using load_documents.py
- Split the pages into smaller chunks using chunk_documents.py
- Create embeddings and store them in ChromaDB using index_chunks.py 
- Search the best matching chunks using hybrid_search.py
- Generate the answer using generate_answer.py

"""

from load_documents import load_documents
from chunk_documents import chunk_documents
from index_chunks import index_chunks
from keyword_search import keyword_search
from semantic_search import semantic_search
from hybrid_search import hybrid_search
from generate_answer import generate_answer


# List with PDFs location
pdf_paths = ["data/ESR-5019.pdf", "data/ETA-26:0367.pdf"]

# Load documents
pages = load_documents(pdf_paths)

# Create chunks
chunks = chunk_documents(pages)

# Create embeddings and store them in ChromaDB
index_chunks(chunks)

# User query 
query = "What installation torque is required for MT-TL M10 OC?"

# Search the best matching chunks with keyword search BM25
#keyword_results, keyword_scores = keyword_search(query, chunks, top_k=20)


# Search the best matching chunks with semantic search
# semantic_result = semantic_search(query, top_k=20)


# Search the best matching chunks with hybrid search
hybrid_result = hybrid_search(query, chunks, top_k=5)

# Generate the answer with the LLM
answer = generate_answer(query, hybrid_result)
print(f"Answer: {answer}")

