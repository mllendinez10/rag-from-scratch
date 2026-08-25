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
from hybrid_search import hybrid_search
from generate_answer import generate_answer


# ---------------------------------------------------------
# Prepare RAG. Runs once to avoid repeated indexing
# ---------------------------------------------------------

def prepare_rag():

    # List with PDFs location
    pdf_paths = ["data/ESR-5019.pdf", "data/ETA-26:0367.pdf"]

    # Load documents    
    pages = load_documents(pdf_paths)

    # Create chunks
    chunks = chunk_documents(pages)

    # Create embeddings and store them in ChromaDB
    index_chunks(chunks)
    
    return chunks
    

# ---------------------------------------------------------
# Run the pipeline. Runs every time app.py calls it
# ---------------------------------------------------------
    
def run_rag_pipeline(query, chunks):

    # Search the best matching chunks with hybrid search
    hybrid_result = hybrid_search(query, chunks, top_k=5)

    # Generate the answer with the LLM
    answer = generate_answer(query, hybrid_result)
    
    return answer, hybrid_result

