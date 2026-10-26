# rag-from-scratch

This project focuses on learning how Retrieval-Augmented Generation (RAG) works by building the complete pipeline from scratch in Python.

It intentionally avoids frameworks such as LangChain and LangGraph at the beginning, so each part of the pipeline can be implemented and understood independently.

As a practical use case, the project uses publicly available Hilti product documentation to build a small product knowledge base and answer product-related questions using retrieved information.

## Project Goal

The goal is to gain hands-on experience with the main components of a RAG system:

- Document loading and text extraction
- Fixed-size text chunking with overlap
- Structure-aware chunking with Docling (optional)
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

| Area                                 | Technology                     |
| ------------------------------------ | ------------------------------ |
| Programming language                 | Python                         |
| PDF extraction                       | PyPDF                          |
| Text chunking                        | Fixed-size chunks with overlap |
| Structure-aware chunking (optional) | Docling                        |
| Keyword retrieval                    | BM25                           |
| Semantic retrieval                   | Sentence Transformers          |
| Embedding model                      | all-MiniLM-L6-v2               |
| Vector database                      | ChromaDB                       |
| Hybrid ranking                       | Reciprocal Rank Fusion (RRF)   |
| LLM                                  | Qwen3 4B via Ollama            |
| Evaluation                           | Hit@K and MRR                  |
| UI                                   | Streamlit                      |

## Project Structure

```text
rag-from-scratch/
│
├── data/
│   ├── ESR-5019.pdf
│   └── ETA-26:0367.pdf
│
├── evaluation/
│   ├── golden_set.json
│   ├── golden_set_docling.json
│   └── rag_retrieval_evaluation_tracker.xlsx
│
├── chroma_db/
│   └── Persistent ChromaDB vector database
│
├── src/
│   ├── app.py
│   ├── load_documents.py
│   ├── chunk_documents.py
│   ├── load_and_chunk_docling.py
│   ├── index_chunks.py
│   ├── keyword_search.py
│   ├── semantic_search.py
│   ├── hybrid_search.py
│   ├── generate_answer.py
│   ├── evaluation.py
│   └── main.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## File Purpose

| File                                 | Purpose                                                                                       |
| ------------------------------------ | --------------------------------------------------------------------------------------------- |
| load_documents.py                    | Loads the PDF documents and extracts the text page by page                                    |
| chunk_documents.py                   | Splits the extracted text into smaller overlapping chunks and keeps the related metadata      |
| index_chunks.py                      | Creates embeddings for the chunks and stores them in ChromaDB                                 |
| keyword_search.py                    | Searches the chunks using BM25 keyword search                                                 |
| semantic_search.py                   | Creates an embedding for the user query and searches ChromaDB for semantically similar chunks |
| hybrid_search.py                     | Combines keyword and semantic search results using Reciprocal Rank Fusion (RRF)               |
| generate_answer.py                   | Uses the retrieved chunks to build a prompt and generate the final LLM answer                 |
| evaluation.py                        | Evaluates retrieval quality using a golden set of questions with Hit@K and MRR metrics        |
| main.py                              | Connects and runs the individual steps of the RAG pipeline                                    |
| app.py                               | Provides the Streamlit user interface                                                         |
| load_and_chunk_docling.py (optional) | Structure-aware chunking with Docling                                                         |

## Docling Chunking Experiment

Docling's structure-aware chunking was tested as an alternative to the existing fixed-size chunking approach.

Docling improved keyword retrieval, but semantic and hybrid retrieval performed worse than with fixed-size chunking. The experiment showed that more sophisticated chunking does not automatically lead to better retrieval quality.

The Docling experiment is kept as an optional alternative ingestion path in `load_and_chunk_docling.py`.

To test it:

1. Install the project requirements, including Docling.
2. Use `load_and_chunk_docling.py` instead of the standard `load_documents.py` + `chunk_documents.py` flow.
3. Store the Docling chunks in a separate ChromaDB collection, for example `document_chunks_docling`.
4. Point semantic and hybrid search to the Docling collection.
5. Use the included `golden_set_docling.json` for the Docling evaluation.
6. Run the same retrieval evaluation and compare the results with the fixed-size baseline.

The Docling experiment was not adopted as the default pipeline because semantic and hybrid retrieval performed worse on this dataset.

## Evaluation Results

Fixed-size chunking with overlap:

| Retrieval |  Hit@1 |  Hit@3 |  Hit@5 | Hit@10 |   MRR |
| --------- | -----: | -----: | -----: | -----: | ----: |
| Keyword   |  0.00% |  0.00% |  0.00% | 14.29% | 0.024 |
| Semantic  | 57.14% | 57.14% | 57.14% | 57.14% | 0.571 |
| Hybrid    |  0.00% | 14.29% | 42.86% |      - | 0.119 |

Docling:

| Retrieval |  Hit@1 |  Hit@3 |  Hit@5 | Hit@10 |   MRR |
| --------- | -----: | -----: | -----: | -----: | ----: |
| Keyword   | 28.57% | 28.57% | 28.57% | 28.57% | 0.286 |
| Semantic  |  0.00% |  0.00% |  0.00% | 28.57% | 0.040 |
| Hybrid    |  0.00% | 28.57% | 28.57% |      - | 0.119 |

Hybrid Hit@10 was not measured because hybrid search returned only 5 results.

## Project Takeaways

The main insights gained from building and evaluating the RAG pipeline from scratch are:

* Retrieval quality is often the main limitation of a RAG system.
* Semantic, keyword, and hybrid retrieval behave differently depending on the question.
* Hybrid retrieval does not automatically outperform semantic or keyword retrieval.
* Technical tables and exact identifiers can be difficult to retrieve reliably with standard text chunking.
* The LLM you choose can make a big difference in answer quality, but larger models also need more computing power to run locally.
* Evaluation is necessary to determine whether a retrieval change actually improves the system.
* More sophisticated chunking does not automatically improve RAG retrieval. Changes should be evaluated with data before being adopted.

## Getting Started

Run all commands from the project root with your virtual environment active.
1. Install dependencies: pip install -r requirements.txt
2. Install and run Ollama, then download the model: ollama pull qwen3:4b
3. Index the document chunks and store their embeddings in ChromaDB: python src/index_chunks.py
4. If you change the documents:
   - Add the new PDFs to data/ and update the document paths.
   - Run python src/index_chunks.py again.
   - Update evaluation/golden_set.json with questions and expected answers from the new documents.
5. Run the pipeline: python src/main.py
6. Launch the UI: streamlit run src/app.py
7. Evaluate retrieval: python src/evaluation.py
