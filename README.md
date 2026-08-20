# rag-from-scratch

This project focuses on learning how Retrieval-Augmented Generation (RAG) works by building the complete pipeline from scratch in Python.

It intentionally avoids frameworks such as LangChain and LangGraph at the beginning, so each part of the pipeline can be implemented and understood independently.

As a practical use case, the project uses publicly available Hilti product documentation to build a small product knowledge base and answer product-related questions using retrieved information.


**Project Goal**

The goal is to gain hands-on experience with the main components of a RAG system:

- Document loading and text extraction
- Text chunking
- Keyword search with BM25
- Semantic search with embeddings and vector storage
- Hybrid search with Reciprocal Rank Fusion (RRF)
- Prompt construction
- LLM answer generation
- UI with Streamlit
- Retrieval evaluation


**Technology Stack**

- Programming language: Python
- PDF extraction: PyPDF
- Keyword retrieval: BM25
- Embeddings: Sentence Transformers
- Vector database: ChromaDB
- Hybrid ranking: Reciprocal Rank Fusion (RRF)
- LLM: Qwen3 8B via Ollama
- UI: Streamlit

**Project Structure**

rag-from-scratch/
│
├── data/
│
├── src/
│   ├── load_documents.py
│   ├── chunk_documents.py
│   ├── keyword_search.py
│   ├── semantic_search.py
│   ├── hybrid_search.py
│   ├── generate_answer.py
│   └── evaluation.py
│
├── main.py
├── app.py
├── requirements.txt
└── README.md