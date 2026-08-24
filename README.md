# rag-from-scratch

This project focuses on learning how Retrieval-Augmented Generation (RAG) works by building the complete pipeline from scratch in Python.

It intentionally avoids frameworks such as LangChain and LangGraph at the beginning, so each part of the pipeline can be implemented and understood independently.

As a practical use case, the project uses publicly available Hilti product documentation to build a small product knowledge base and answer product-related questions using retrieved information.

## Project Goal

The goal is to gain hands-on experience with the main components of a RAG system:

- Document loading and text extraction
- Fixed-size text chunking with overlap
- Keyword search using BM25
- Embedding generation
- Vector storage using ChromaDB
- Semantic vector search
- Hybrid search using Reciprocal Rank Fusion (RRF)
- Prompt construction
- LLM answer generation
- Retrieval evaluation using a golden set
- UI development with Streamlit

## Technology Stack

| Area                 | Technology                     |
| -------------------- | ------------------------------ |
| Programming language | Python                         |
| PDF extraction       | PyPDF                          |
| Text chunking        | Fixed-size chunks with overlap |
| Keyword retrieval    | BM25                           |
| Semantic retrieval   | Sentence Transformers          |
| Embedding model      | all-MiniLM-L6-v2               |
| Vector database      | ChromaDB                       |
| Hybrid ranking       | Reciprocal Rank Fusion (RRF)   |
| LLM                  | Qwen3 4B via Ollama            |
| Evaluation           | Hit@K and MRR                  |
| UI                   | Streamlit                      |

## Project Structure

```text
rag-from-scratch/
│
├── data/
│   └── PDF documents
│
├── evaluation/
│   ├── golden_set.json
│   └── rag_retrieval_evaluation_tracker.xlsx
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

| File               | Purpose                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------- |
| load_documents.py  | Loads the PDF documents and extracts the text page by page                                    |
| chunk_documents.py | Splits the extracted text into smaller overlapping chunks and keeps the related metadata      |
| index_chunks.py    | Creates embeddings for the chunks and stores them in ChromaDB                                 |
| keyword_search.py  | Searches the chunks using BM25 keyword search                                                 |
| semantic_search.py | Creates an embedding for the user query and searches ChromaDB for semantically similar chunks |
| hybrid_search.py   | Combines keyword and semantic search results using Reciprocal Rank Fusion (RRF)               |
| generate_answer.py | Uses the retrieved chunks to build a prompt and generate the final LLM answer                 |
| evaluation.py      | Evaluates retrieval quality using a golden set of questions with Hit@K and MRR metrics        |
| main.py            | Connects and runs the individual steps of the RAG pipeline                                    |
| app.py             | Provides the Streamlit user interface                                                         |

## Project takeaways

The main insights gained from building and evaluating the RAG pipeline from scratch are:

* Retrieval quality is often the main limitation of a RAG system.
* Semantic, keyword, and hybrid retrieval behave differently depending on the question.
* Hybrid retrieval does not automatically outperform semantic or keyword retrieval.
* Technical tables and exact identifiers can be difficult to retrieve reliably with standard text chunking.
* The LLM you choose can make a big difference in answer quality, but larger models also need more computing power to run locally.
* Evaluation is necessary to determine whether a retrieval change actually improves the system.
