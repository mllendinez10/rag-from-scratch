"""
Generate an answer using the results from hybrid search.

This script will:
- Receive the user query
- Receive the hybrid search results
- Combine the retrieved chunk text, from hybrid search, into context
- Create a prompt for the LLM
- Send the prompt to the LLM
- Return the generated answer
"""

import ollama

# Local LLM model
LLM_MODEL = "qwen3:4b"

def generate_answer(query, hybrid_result):
    
    # ---------------------------------------------------------
    # Prompt creation
    # ---------------------------------------------------------
    
    # Combine the text from the hybrid search results into one context
    context = ""

    for chunk in hybrid_result:
        context += chunk["text"] + "\n\n"

    # Create the prompt for the LLM
    prompt = f"""
Use only the following context to answer the question.

If the answer cannot be found in the context, say that the information
is not available in the provided documents.

Context:
{context}

Question:
{query}

Answer:
"""

    # ---------------------------------------------------------
    # LLM call
    # ---------------------------------------------------------
    
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return response["message"]["content"]