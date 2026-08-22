"""
Hybrid search using Reciprocal Rank Fusion (RRF)

This script will:
- Receive the results from keyword_search.py and semantic_search.py
- Homogenize the results so that RRF can be applied
- Apply RRF
- Return the result from hybrid search
"""


from keyword_search import keyword_search
from semantic_search import semantic_search


def hybrid_search (query, chunks, top_k=5):

    # Get result from keyword search
    keyword_result, keyword_score = keyword_search(query, chunks, top_k)

    # Get result from semantic search
    semantic_result = semantic_search(query, chunks, top_k)

    """ 
    The results from keyword and semantic search have a different format.
    So they need to be homogenized before using RRF.
    For RRF all we need is the chunk number or ID and its possition.
    """

    # ---------------------------------------------------------
    # Homogenize keyword and semantic search
    # ---------------------------------------------------------

    # Homogenize keyword

    keyword_homogenized = []

    keyword_chunk_id = keyword_result[0] # Extract The first list within the list

    keyword_rank = 1

    for chunk_id in keyword_chunk_id:
        keyword_homogenized.append({
            "chunk_id": str(chunk_id),
            "rank": keyword_rank
            })
        keyword_rank += 1


    # Homogenize semantic search

    semantic_homogenized = []

    semantic_chunk_id = semantic_result["ids"][0] # Extract the first list within the "ids" list

    semantic_rank = 1

    for chunk_id in semantic_chunk_id:
        semantic_homogenized.append({
            "chunk_id": str(chunk_id),
            "rank": semantic_rank
            })
        semantic_rank += 1


    # ---------------------------------------------------------
    # Apply RRF
    # ---------------------------------------------------------
    
    rrf_scores = {}

    # Process keyword search result

    for result in keyword_homogenized:
        chunk_id = result["chunk_id"]
        rank = result["rank"]

        if chunk_id not in rrf_scores:
             rrf_scores[chunk_id] = 0

        rrf_scores[chunk_id] +=1 / (60 + rank)


    # Process semantic search result
    
    for result in semantic_homogenized:
        chunk_id = result["chunk_id"]
        rank = result["rank"]
    
        if chunk_id not in rrf_scores:
            rrf_scores[chunk_id] = 0
    
        rrf_scores[chunk_id] +=1 / (60 + rank)


    # Sort by highest RRF score

    sorted_results = sorted(
        rrf_scores.items(),
        key=lambda item: item[1],
        reverse=True
        )

    # ---------------------------------------------------------
    # Calculate hybrid results
    # ---------------------------------------------------------


    hybrid_result = []

    for chunk_id, score in sorted_results[:top_k]:

        for chunk in chunks: # metadata will be taken from original chunks

             if str(chunk["chunk"]) == chunk_id:

                hybrid_result.append({
                "chunk_id": chunk_id,
                "rrf_score": score,

                # take from original chunk
                "text": chunk["text"], 
                "source": chunk["source"],
                "page": chunk["page"],
                })

                break

    return hybrid_result