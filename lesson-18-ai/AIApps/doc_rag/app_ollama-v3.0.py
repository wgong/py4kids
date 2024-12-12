import streamlit as st
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM  # Updated imports
from PyPDF2 import PdfReader
from typing import List
import os

ollama_model_name = "llama3"
ollama_base_url: str = "http://localhost:11434"

class StreamHandler:
    """Handler for streaming LLM responses to Streamlit"""
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Callback function to handle new tokens"""
        self.text += token
        self.container.message(self.text, is_user=False)

def load_documents(uploaded_files: List) -> str:
    """Load and combine text from multiple PDF documents"""
    text = ""
    for pdf in uploaded_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def setup_rag_chain(text: str, persist_directory: str, ollama_url: str = ollama_base_url):
    """Set up the RAG pipeline with document processing and Chroma vector storage"""
    # Initialize models with updated classes
    embeddings = OllamaEmbeddings(
        model=ollama_model_name, 
        base_url=ollama_url
    )
    
    llm = OllamaLLM(  # Changed from Ollama to OllamaLLM
        model=ollama_model_name,
        base_url=ollama_url,
        temperature=0.5
    )

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Create or load vector store
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectorstore.persist()  # Save the embeddings to disk

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

def main():
    st.set_page_config(page_title="Chat with Doc", page_icon="📚")
    st.header("📚 Chat with Doc")

    # Initialize chat history
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

    # File upload - allow multiple files
    uploaded_files = st.file_uploader(
        "Upload your PDF files",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:
        # Process documents
        if "qa_chain" not in st.session_state:
            with st.spinner("Processing documents..."):
                text = load_documents(uploaded_files)
                qa_chain = setup_rag_chain(text, persist_dir, ollama_url)
                st.session_state["qa_chain"] = qa_chain
                st.success("Documents processed! You can now ask questions.")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if query := st.chat_input("Ask a question about your documents:"):
        if "qa_chain" in st.session_state:
            # Display user message
            st.chat_message("user").markdown(query)
            st.session_state.messages.append({"role": "user", "content": query})

            # Display assistant response with spinner
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                stream_handler = StreamHandler(response_placeholder)
                
                response = st.session_state["qa_chain"].run(
                    query,
                    callbacks=[stream_handler]
                )
                
                # Add assistant's response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.warning("Please upload PDF documents first.")

if __name__ == "__main__":
    main()