import streamlit as st
import time

from main import prepare_rag, run_rag_pipeline


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("RAG Assistant")
st.caption("Ask about the products")


# --------------------------------------------------
# Prepare RAG once and reuse the prepared chunks
# --------------------------------------------------

@st.cache_resource
def load_rag():
    return prepare_rag()


chunks = load_rag()


# --------------------------------------------------
# Initialize chat history for the current session
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# Display previous messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# --------------------------------------------------
# User input
# --------------------------------------------------

query = st.chat_input(
    "Ask a question..."
)


# --------------------------------------------------
# Process question
# --------------------------------------------------

if query:

    # Show user message
    with st.chat_message("user"):
        st.write(query)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    # Run RAG pipeline
    with st.spinner("Searching documents..."):
    
        start_time = time.time()
        
        answer, hybrid_results = run_rag_pipeline(query, chunks)
        
        elapsed_time = time.time() - start_time
        

    # Show assistant answer and running time
    with st.chat_message("assistant"):
        st.write(answer)
        st.caption(f"Generated in {elapsed_time:.2f} seconds")

    # Save assistant answer
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Show sources
    with st.expander("Sources"):

        for rank, chunk in enumerate(hybrid_results, start=1):

            st.markdown(
                f"**Source {rank}: {chunk['source']} — page {chunk['page']}**"
            )

            st.write(chunk["text"])

            st.divider()

