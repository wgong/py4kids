import streamlit as st
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from PyPDF2 import PdfReader
from typing import List
import json
import os
import hashlib
# from stream_handler import StreamHandler  # Import StreamHandler from helper module
from langchain_core.callbacks import BaseCallbackHandler

ollama_model_name = "llama3" # "phi3.5"  # 
ollama_base_url: str = "http://localhost:11434"

class StreamHandler(BaseCallbackHandler):
    """Handler for streaming LLM responses to Streamlit"""
    
    def __init__(self, container):
        """Initialize the handler with a container for displaying text."""
        self.container = container
        self.text = ""
        self.raise_error = False
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.text += token
        # Handle potential JSON in response
        try:
            # Try to parse as JSON
            response_dict = json.loads(self.text)
            display_text = response_dict.get('result', '') or response_dict.get('answer', '') or self.text
            self.container.markdown(display_text)
        except json.JSONDecodeError:
            # Not JSON, display as is
            self.container.markdown(self.text)

def get_document_hash(file) -> str:
    """Generate a hash for a document to track processed files"""
    content = file.read()
    file.seek(0)  # Reset file pointer
    return hashlib.md5(content).hexdigest()

@st.cache_data
def load_documents(uploaded_files: List) -> str:
    """Load and combine text from multiple PDF documents"""
    text = ""
    for pdf in uploaded_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

@st.cache_resource
def get_existing_vectorstore(persist_directory: str, _embeddings):
    """Try to load existing vector store"""
    if os.path.exists(persist_directory) and os.path.isdir(persist_directory):
        try:
            return Chroma(persist_directory=persist_directory, embedding_function=_embeddings)
        except Exception as e:
            st.error(f"Error loading existing vector store: {str(e)}")
            return None
    return None

def setup_rag_chain(text: str, persist_directory: str, ollama_url: str = ollama_base_url):
    """Set up the RAG pipeline with document processing and Chroma vector storage"""
    # Initialize embeddings
    embeddings = OllamaEmbeddings(
        model=ollama_model_name, 
        base_url=ollama_url
    )
    
    # Try to load existing vector store
    vectorstore = get_existing_vectorstore(persist_directory, _embeddings=embeddings)
    
    if text:  # If new text is provided, add it to vector store
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Reduce from 1000 to 500
            chunk_overlap=50,  # Reduce from 200 to 50
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        if vectorstore is None:
            # Create new vector store if none exists
            vectorstore = Chroma.from_texts(
                texts=chunks,
                embedding=embeddings,
                persist_directory=persist_directory
            )
        else:
            # Add new documents to existing vector store
            vectorstore.add_texts(chunks)
        
        vectorstore.persist()  # Save the embeddings to disk
    
    if vectorstore is None:
        st.error("No vector store available. Please upload documents.")
        return None

    # Initialize LLM
    llm = OllamaLLM(
        model=ollama_model_name,
        base_url=ollama_url,
        temperature=0.5
    )

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    
    return qa_chain

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()
    if "qa_cache" not in st.session_state:  # Add cache to session state
        st.session_state.qa_cache = {}        

def main():
    st.set_page_config(page_title="Chat with Doc", page_icon="📚")
    st.header("📚 Chat with Doc")

    # Initialize chat history and processed files tracking
    initialize_chat_history()

    # Configure Ollama
    ollama_url = st.sidebar.text_input(
        "Ollama Base URL",
        value=ollama_base_url,
        help="Enter your Ollama server URL"
    )

    # Set up persistent storage directory
    persist_dir = "chroma_db"
    os.makedirs(persist_dir, exist_ok=True)

    # First, try to load existing vector store and set up qa_chain
    if "qa_chain" not in st.session_state:
        qa_chain = setup_rag_chain("", persist_dir, ollama_url)
        if qa_chain:
            st.session_state["qa_chain"] = qa_chain
            st.success("Loaded existing documents. You can ask questions.")

    # File upload - allow multiple files
    uploaded_files = st.file_uploader(
        "Upload your PDF files",
        type="pdf",
        accept_multiple_files=True
    )

    # Handle new file uploads
    if uploaded_files:
        # Check for new files
        current_files = {get_document_hash(f) for f in uploaded_files}
        new_files = [f for f in uploaded_files if get_document_hash(f) not in st.session_state.processed_files]
        
        if new_files:
            with st.spinner("Processing new documents..."):
                text = load_documents(new_files)
                qa_chain = setup_rag_chain(text, persist_dir, ollama_url)
                if qa_chain:
                    st.session_state["qa_chain"] = qa_chain
                    st.session_state.processed_files.update(current_files)
                    st.success("New documents processed and added!")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if query := st.chat_input("Ask a question about your documents:"):
        if "qa_chain" in st.session_state:
            # Check if question was asked before
            if query in st.session_state.qa_cache:
                # Use cached response
                cached_response = st.session_state.qa_cache[query]
                st.chat_message("user").markdown(query)
                st.session_state.messages.append({"role": "user", "content": query})
                
                with st.chat_message("assistant"):
                    st.markdown(cached_response)
                st.session_state.messages.append({"role": "assistant", "content": cached_response})
            else:
                # Generate new response
                st.chat_message("user").markdown(query)
                st.session_state.messages.append({"role": "user", "content": query})

                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    stream_handler = StreamHandler(response_placeholder)
                    
                    with st.spinner('Generating response...'):
                        try:
                            response = st.session_state["qa_chain"].invoke(
                                query,
                                config={'callbacks': [stream_handler]}
                            )
                            
                            # Extract text from response if it's a dict
                            if isinstance(response, dict):
                                response = response.get('result', '') or response.get('answer', '') or str(response)
                            
                            # Cache the new response
                            st.session_state.qa_cache[query] = response
                            
                            # Add assistant's response to chat history
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        except Exception as e:
                            st.error(f"Error generating response: {str(e)}")
            
if __name__ == "__main__":
    main()