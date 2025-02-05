import groq
import streamlit as st
from streamlit_chat import message  # Ensure streamlit-chat is installed
import PyPDF2
import faiss
import numpy as np

def initialize_groq_client(api_key):
    """Initialize the Groq API client"""
    client = groq.Client(api_key=api_key)
    return client

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def index_corpus(corpus):
    """Index the text corpus using FAISS"""
    # Convert the text into embeddings (dummy embeddings here for simplicity)
    # You can replace this with any method of converting text to embeddings.
    embeddings = np.random.rand(len(corpus), 512).astype('float32')  # Dummy embeddings
    index = faiss.IndexFlatL2(512)  # Dimensionality of embeddings
    index.add(embeddings)
    return index, embeddings

def retrieve_documents(query, index, corpus):
    """Retrieve relevant documents based on the user's query"""
    # Convert query into embedding (dummy embedding here)
    query_embedding = np.random.rand(1, 512).astype('float32')  # Dummy embedding for query
    _, indices = index.search(query_embedding, k=3)  # Retrieve top 3 most relevant documents
    return [corpus[i] for i in indices[0]]

def chat_with_groq(client, conversation_history):
    """Send conversation history to the Groq model and return a response"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Replace with a locally hosted model if available
        messages=conversation_history,
        max_tokens=200
    )
    return response.choices[0].message.content

def generate_answer(user_query, retrieved_docs, client):
    """Combine the query with retrieved documents and generate an answer"""
    input_text = user_query + " " + " ".join(retrieved_docs)
    
    # Send the input text along with previous conversation history to the Groq model
    conversation_history = [{"role": "user", "content": input_text}]
    response = chat_with_groq(client, conversation_history)
    return response

st.title("Groq Messenger Chatbot with RAG")
st.warning("Ensure you have installed 'streamlit-chat' using: pip install streamlit-chat")

api_key = st.text_input("Enter Groq API Key", type="password")
pdf_file = st.file_uploader("Upload Knowledge Base PDF", type="pdf")

if api_key and pdf_file:
    # Initialize the Groq client
    client = initialize_groq_client(api_key)
    
    # Extract text from PDF and index it
    corpus_text = extract_text_from_pdf(pdf_file)
    corpus = corpus_text.split("\n")  # Split the text into sentences or paragraphs
    index, _ = index_corpus(corpus)
    
    # Initialize conversation history in session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    
    for msg in st.session_state.conversation:
        message(msg["content"], is_user=(msg["role"] == "user"))
    
    user_input = st.text_input("Type a message...")
    
    if st.button("Send") and user_input:
        # Retrieve relevant documents from the knowledge base
        retrieved_docs = retrieve_documents(user_input, index, corpus)
        
        # Generate the response using the retrieved documents and the Groq model
        response = generate_answer(user_input, retrieved_docs, client)
        
        # Append user input and Groq's response to conversation history
        st.session_state.conversation.append({"role": "user", "content": user_input})
        st.session_state.conversation.append({"role": "assistant", "content": response})
        
        # Rerun the app to display the conversation
        st.rerun()
