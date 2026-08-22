"""
Create embeddings for document chunks and store them in ChromaDB.

This script will:
- Receive the document chunks
- Extract the chunk text
- Prepare chunk IDs and metadata
- Create embeddings for the chunk text
- Store the chunks and embeddings in ChromaDB
"""

import chromadb
from sentence_transformers import SentenceTransformer

# Where Chroma stores the vector database
CHROMA_PATH = "./chroma_db"

# A Chroma collection is similar to a table in SQL
COLLECTION_NAME = "document_chunks"

# Model that converts text into vectors
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load embedding model, it will be used for the chunks
model = SentenceTransformer(EMBEDDING_MODEL)

# Create connection to ChromaDB. PersistentClient means that it stores everything on disk and not memmory
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create collection in ChromaDB
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def index_chunks(chunks):
    
    # List with chunks text
    chunks_texts = []
    
    # List with chunks numbers. In ChromaDB it is the ID equivalent.
    chunks_ids = []
    
    # List with dictionary of chunks metadata (source and page). ChromaDB only has one metadata field.
    chunks_metadata = []
    
    # Go through the chunks and prepare data for ChromaDB
    for chunk in chunks:
        chunks_texts.append(chunk["text"])
        chunks_ids.append(str(chunk["chunk"])) #ID must be a string
        chunks_metadata.append({
            "source": chunk["source"],
            "page": chunk["page"]
            })
      
    # Create chunks embeddings
    chunks_embeddings = model.encode(chunks_texts, convert_to_numpy=True)
    
    # Store lists in ChromaDB fields 
    collection.upsert(
        ids=chunks_ids,
        documents=chunks_texts,
        embeddings=chunks_embeddings.tolist(), # needs to be a list
        metadatas=chunks_metadata
        )
    
    # Nothing needs to be returned