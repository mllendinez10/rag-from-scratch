"""
Search document chunks using keyword-based BM25 ranking.

This script will:
- Receive the document chunks
- Extract the text from each chunk
- Tokenize the chunk text
- Tokenize the user query
- Create the BM25 search object
- Build the BM25 index
- Search the indexed chunks
- Return the best matching chunk indexes and their BM25 scores

"""

import bm25s

def keyword_search(query, chunks, top_k=5):
    
    # List with only the text from each chunk
    chunks_text = []
    
    for chunk in chunks:
        chunks_text.append(chunk["text"])
        
    # Tokenize all chunk texts so BM25 can work with individual words
    chunks_text_tokenized = bm25s.tokenize(chunks_text)
    
     # Tokenize query
    query_tokenized = bm25s.tokenize(query)
    
    # Create the BM25 search object
    retriever = bm25s.BM25()
    
    # Build the BM25 search index using the tokenized chunks
    retriever.index(chunks_text_tokenized)
    
    # Search the BM25 index and return the best matching chunks
    results, scores = retriever.retrieve( query_tokenized, k=top_k)
    
    return results, scores