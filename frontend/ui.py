import streamlit as st
import requests
import json

# Streamlit UI
st.title("AI Customer Support Chatbot")
st.write("Ask me anything about our services!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    try:
        response = requests.post(
            "http://localhost:8000/api/chat/",
            json={"query": prompt},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            ai_response = response.json()["response"]
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            with st.chat_message("assistant"):
                st.markdown(ai_response)
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error occurred')}")
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")

# Add a sidebar with information
with st.sidebar:
    st.title("About")
    st.write("""
    This AI Customer Support Chatbot uses:
    - Mixtral 8x7B on Groq for answering queries
    - FAISS with MPNET embeddings for semantic search
    - LangChain for RAG (retrieval-augmented generation)
    - Django backend for processing
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
