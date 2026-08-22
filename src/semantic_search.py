"""
Search the stored document chunks using semantic vector search.

This script will:
- Receive a user query
- Create an embedding for the query
- Search ChromaDB for the most similar chunk vectors
- Return the most relevant results

"""

import chromadb
from sentence_transformers import SentenceTransformer

# Where Chroma stores the vector database
CHROMA_PATH = "./chroma_db"

# A Chroma collection is similar to a table in SQL
COLLECTION_NAME = "document_chunks"

# Model that converts text into vectors
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load embedding model, it will be used for the query
model = SentenceTransformer(EMBEDDING_MODEL)

# Create connection to ChromaDB. PersistentClient means that it stores everything on disk and not memmory
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create collection in ChromaDB
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def semantic_search (query, top_k=5):

    # Create query embedding
    query_embedding = model.encode(query, convert_to_numpy=True)

    # Search in ChromaDB for the most semantically similar chunks
    results = collection.query(
        query_embeddings = [query_embedding.tolist()],
        n_results = top_k
    )

    return results