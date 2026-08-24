"""
Evaluate the retrieval performance of the RAG pipeline.

This script will:
- Load the evaluation questions from the golden set
- Load and chunk the source documents
- Run BM25, semantic, and hybrid search
- Compare the retrieved chunks with the relevant chunks
- Calculate retrieval metrics
"""

import json

from load_documents import load_documents
from chunk_documents import chunk_documents
from keyword_search import keyword_search
from semantic_search import semantic_search
from hybrid_search import hybrid_search


# ---------------------------------------------------------
# Load documents and create chunks
# ---------------------------------------------------------

# List with PDFs location
pdf_paths = ["data/ESR-5019.pdf", "data/ETA-26:0367.pdf"]

# Load documents
pages = load_documents(pdf_paths)

# Create chunks
chunks = chunk_documents(pages)


# ---------------------------------------------------------
# Load golden set
# ---------------------------------------------------------

# Open and store json file
with open("evaluation/golden_set.json", "r", encoding="utf-8") as file:
    golden_set = json.load(file)
    
# Test
print(f"the loaded file contains: {len(golden_set)} questions")


# ---------------------------------------------------------
# Evaluation counters
# ---------------------------------------------------------

keyword_hit_1 = 0
keyword_hit_3 = 0
keyword_hit_5 = 0
keyword_hit_10 = 0


semantic_hit_1 = 0
semantic_hit_3 = 0
semantic_hit_5 = 0
semantic_hit_10 = 0


hybrid_hit_1 = 0
hybrid_hit_3 = 0
hybrid_hit_5 = 0
hybrid_hit_10 = 0

keyword_mrr = 0
semantic_mrr = 0
hybrid_mrr = 0

# ---------------------------------------------------------
# Loop through golden questions 
# Return chunk IDs from keyword, semantic and hybrid search
# ---------------------------------------------------------

for item in golden_set:
    
    # Print questions and relevant chunks IDs from the golden set
    query = item["question"]
    relevant_chunk_ids = item["relevant_chunk_ids"]
    
    print("\n" + "-" * 80)
    print(f"Question: {query}")
    print(f"Relevant chunks: {relevant_chunk_ids}")
    
    # Keyword search
    keyword_results, keyword_scores = keyword_search(query, chunks, top_k=10)
    
    # Convert result into a single list
    keyword_ids = []

    for chunk_id in keyword_results[0]:
        keyword_ids.append(str(chunk_id))
        
    print(f"Keyword retrieved chunks: {keyword_ids}")
    
    # semantic search
    semantic_result = semantic_search(query, top_k=10)
    
    # Convert result into a single list
    semantic_ids = []

    for chunk_id in semantic_result["ids"][0]:
        semantic_ids.append(str(chunk_id))
        
    print(f"Semantic retrieved chunks: {semantic_ids}")
    
    # hybrid search
    hybrid_result = hybrid_search(query, chunks, top_k=5)
        
    # Convert result into a single list
    hybrid_ids = []

    for result in hybrid_result:
        hybrid_ids.append(result["chunk_id"])
            
    print(f"Hybrid retrieved chunks: {hybrid_ids}")
    
    
    # -----------------------------------------------------
    # Hit@K evaluation
    # -----------------------------------------------------

    # Keyword
    if any(chunk_id in keyword_ids[:1] for chunk_id in relevant_chunk_ids):
        keyword_hit_1 += 1

    if any(chunk_id in keyword_ids[:3] for chunk_id in relevant_chunk_ids):
        keyword_hit_3 += 1

    if any(chunk_id in keyword_ids[:5] for chunk_id in relevant_chunk_ids):
        keyword_hit_5 += 1
        
    if any(chunk_id in keyword_ids[:10] for chunk_id in relevant_chunk_ids):
            keyword_hit_10 += 1


    # Semantic
    if any(chunk_id in semantic_ids[:1] for chunk_id in relevant_chunk_ids):
        semantic_hit_1 += 1

    if any(chunk_id in semantic_ids[:3] for chunk_id in relevant_chunk_ids):
        semantic_hit_3 += 1

    if any(chunk_id in semantic_ids[:5] for chunk_id in relevant_chunk_ids):
        semantic_hit_5 += 1
        
    if any(chunk_id in semantic_ids[:10] for chunk_id in relevant_chunk_ids):
            semantic_hit_10 += 1


    # Hybrid
    if any(chunk_id in hybrid_ids[:1] for chunk_id in relevant_chunk_ids):
        hybrid_hit_1 += 1

    if any(chunk_id in hybrid_ids[:3] for chunk_id in relevant_chunk_ids):
        hybrid_hit_3 += 1

    if any(chunk_id in hybrid_ids[:5] for chunk_id in relevant_chunk_ids):
        hybrid_hit_5 += 1
        
    if any(chunk_id in hybrid_ids[:10] for chunk_id in relevant_chunk_ids):
        hybrid_hit_10 += 1
        
    
    # -----------------------------------------------------
    # Mean Reciprocal Rank (MRR) evaluation
    # -----------------------------------------------------

    for rank, chunk_id in enumerate(keyword_ids, start=1):
        if chunk_id in relevant_chunk_ids:
            keyword_mrr += 1 / rank
            break

    for rank, chunk_id in enumerate(semantic_ids, start=1):
        if chunk_id in relevant_chunk_ids:
            semantic_mrr += 1 / rank
            break

    for rank, chunk_id in enumerate(hybrid_ids, start=1):
        if chunk_id in relevant_chunk_ids:
            hybrid_mrr += 1 / rank
            break
        

# ---------------------------------------------------------
# Final results
# ---------------------------------------------------------

total_questions = len(golden_set)

print("\n" + "=" * 80)
print("RETRIEVAL EVALUATION")
print("=" * 80)

print("\nKEYWORD")
print(f"Hit@1: {keyword_hit_1 / total_questions:.2%}")
print(f"Hit@3: {keyword_hit_3 / total_questions:.2%}")
print(f"Hit@5: {keyword_hit_5 / total_questions:.2%}")
print(f"Hit@10: {keyword_hit_10 / total_questions:.2%}")
print(f"MRR: {keyword_mrr / total_questions:.3f}")

print("\nSEMANTIC")
print(f"Hit@1: {semantic_hit_1 / total_questions:.2%}")
print(f"Hit@3: {semantic_hit_3 / total_questions:.2%}")
print(f"Hit@5: {semantic_hit_5 / total_questions:.2%}")
print(f"Hit@10: {semantic_hit_10 / total_questions:.2%}")
print(f"MRR: {semantic_mrr / total_questions:.3f}")

print("\nHYBRID")
print(f"Hit@1: {hybrid_hit_1 / total_questions:.2%}")
print(f"Hit@3: {hybrid_hit_3 / total_questions:.2%}")
print(f"Hit@5: {hybrid_hit_5 / total_questions:.2%}")
print(f"Hit@10: {hybrid_hit_10 / total_questions:.2%}")
print(f"MRR: {hybrid_mrr / total_questions:.3f}")