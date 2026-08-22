# rag-from-scratch

This project focuses on learning how Retrieval-Augmented Generation (RAG) works by building the complete pipeline from scratch in Python.

It intentionally avoids frameworks such as LangChain and LangGraph at the beginning, so each part of the pipeline can be implemented and understood independently.

As a practical use case, the project uses publicly available Hilti product documentation to build a small product knowledge base and answer product-related questions using retrieved information.



## Project Goal

The goal is to gain hands-on experience with the main components of a RAG system:

- Document loading and text extraction
- Text chunking with overlap
- Keyword search using BM25
- Embedding generation
- Vector storage using ChromaDB
- Semantic vector search
- Hybrid search using Reciprocal Rank Fusion (RRF)
- Prompt construction
- LLM answer generation
- UI development with Streamlit
- Retrieval evaluation



## Technology Stack

| Area | Technology |
|---|---|
| Programming language | Python |
| PDF extraction | PyPDF |
| Keyword retrieval | BM25 |
| Embeddings | Sentence Transformers |
| Embedding model | all-MiniLM-L6-v2 |
| Vector database | ChromaDB |
| Hybrid ranking | Reciprocal Rank Fusion (RRF) |
| LLM | Qwen3 8B via Ollama |
| UI | Streamlit |



## Project Structure

```text
rag-from-scratch/
│
├── data/
│   └── PDF documents
│
├── chroma_db/
│   └── Persistent vector database
│
├── src/
│   ├── load_documents.py
│   ├── chunk_documents.py
│   ├── index_chunks.py
│   ├── keyword_search.py
│   ├── semantic_search.py
│   ├── hybrid_search.py
│   ├── generate_answer.py
│   ├── evaluation.py
│   └── main.py
│
├── app.py
├── requirements.txt
└── README.md
```


## File Purpose

| File | Purpose |
|---|---|
| load_documents.py | Loads the PDF documents and extracts the text page by page |
| chunk_documents.py | Splits the extracted text into smaller overlapping chunks and keeps the related metadata |
| index_chunks.py | Creates embeddings for the chunks and stores them in ChromaDB |
| keyword_search.py | Searches the chunks using BM25 keyword search |
| semantic_search.py | Creates an embedding for the user query and searches ChromaDB for semantically similar chunks |
| hybrid_search.py | Combines keyword and semantic search results using Reciprocal Rank Fusion (RRF) |
| generate_answer.py | Uses the retrieved chunks to build a prompt and generate the final LLM answer |
| evaluation.py | Evaluates the quality of retrieval and generated answers |
| main.py | Connects and runs the individual steps of the RAG pipeline |
| app.py | Provides the Streamlit user interface |