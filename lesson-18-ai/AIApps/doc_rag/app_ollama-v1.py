import streamlit as st
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from PyPDF2 import PdfReader
from typing import List

ollama_model_name = "llama3"
ollama_url = "http://localhost:11434"

class StreamHandler:
    """Handler for streaming LLM responses to Streamlit"""
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Callback function to handle new tokens"""
        self.text += token
        self.container.markdown(self.text)

def load_documents(uploaded_files: List) -> str:
    """Load and combine text from multiple PDF documents"""
    text = ""
    for pdf in uploaded_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def setup_rag_chain(text: str, ollama_base_url: str = ollama_url):
    """Set up the RAG pipeline with document processing and vector storage"""
    # Initialize models
    embeddings = OllamaEmbeddings(
        model=ollama_model_name,
        base_url=ollama_base_url
    )
    
    llm = Ollama(
        model=ollama_model_name,
        base_url=ollama_base_url,
        temperature=0.5
    )

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Create vector store
    vectorstore = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    
    return qa_chain

def main():
    st.set_page_config(page_title="Chat with PDFs", page_icon="📚")
    st.header("📚 Chat with your PDF documents")

    # Configure Ollama
    ollama_base_url = st.sidebar.text_input(
        "Ollama Base URL",
        value=ollama_url,
        help="Enter your Ollama server URL"
    )

    # File upload - allow multiple files
    uploaded_files = st.file_uploader(
        "Upload your PDF files",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files:
        # Process documents
        with st.spinner("Processing documents..."):
            text = load_documents(uploaded_files)
            qa_chain = setup_rag_chain(text, ollama_base_url)
            st.session_state["qa_chain"] = qa_chain
            st.success("Documents processed! You can now ask questions.")

        # Query input
        query = st.text_input("Ask a question about your documents:")
        if query and "qa_chain" in st.session_state:
            with st.spinner("Generating response..."):
                # Create a placeholder for streaming response
                response_placeholder = st.empty()
                
                # Create stream handler
                stream_handler = StreamHandler(response_placeholder)
                
                # Run query with streaming
                st.session_state["qa_chain"].run(
                    query,
                    callbacks=[stream_handler]
                )

if __name__ == "__main__":
    main()