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
    
/no_think

Use only the following context to answer the question.

Give only the final answer.
Answer directly and concisely.
Do not explain your reasoning.
Do not describe how you searched the context.
Do not repeat the context.
Do not include information that is not supported by the context.

If the answer cannot be found in the context, say:
"The information is not available in the provided documents."

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
        ],
        # Disable Qwen3 thinking mode for faster answers
        think=False,
        # Keep the model loaded in memory for faster follow up questions. It consumes RAM
        keep_alive="10m"
    )
    
    return response["message"]["content"]

