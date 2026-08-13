# rag-from-scratch

This project focuses on learning how RAG works under the hood by implementing the complete pipeline from scratch in Python.

It intentionally avoids frameworks such as LangChain and LangGraph in order to implement and understand each step of the pipeline independently.

The goal is to gain hands-on experience with:

- Document loading and text extraction
- Text chunking strategies
- Embedding generation
- Vector database storage
- Semantic vector search
- Document retrieval
- Prompt construction
- LLM based answer generation

As a practical use case, the project uses publicly available Hilti product documentation to build a small product knowledge base. The system will retrieve relevant information from these documents and answer product related questions using a locally hosted LLM.
