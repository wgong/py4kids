import streamlit as st
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from PyPDF2 import PdfReader
from typing import List, BinaryIO
import os

class StreamHandler:
    """Handler for streaming LLM responses to Streamlit"""
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Callback function to handle new tokens"""
        self.text += token
        self.container.message(self.text, is_user=False)

def read_pdf(file: BinaryIO) -> str:
    """Extract text from PDF file"""
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def read_txt(file: BinaryIO) -> str:
    """Read text from TXT file"""
    return file.read().decode('utf-8')

def read_markdown(file: BinaryIO) -> str:
    """Read text from Markdown file"""
    return file.read().decode('utf-8')

def load_documents(uploaded_files: List) -> str:
    """Load and combine text from multiple documents"""
    text = ""
    for file in uploaded_files:
        # Get file extension
        file_extension = os.path.splitext(file.name)[1].lower()
        
        # Process based on file type
        if file_extension == '.pdf':
            text += read_pdf(file)
        elif file_extension == '.txt':
            text += read_txt(file)
        elif file_extension in ['.md', '.markdown']:
            text += read_markdown(file)
        
        # Add a newline between documents
        text += "\n\n"
    
    return text

def setup_rag_chain(text: str, persist_directory: str, ollama_base_url: str = "http://localhost:11434"):
    """Set up the RAG pipeline with document processing and Chroma vector storage"""
    # Initialize models
    embeddings = OllamaEmbeddings(
        model="llama2", 
        base_url=ollama_base_url
    )
    
    llm = Ollama(
        model="llama2",
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
    st.set_page_config(page_title="Chat with Documents", page_icon="📚")
    st.header("📚 Chat with your Documents")

    # Initialize chat history
    initialize_chat_history()

    # Configure Ollama
    ollama_base_url = st.sidebar.text_input(
        "Ollama Base URL",
        value="http://localhost:11434",
        help="Enter your Ollama server URL"
    )

    # Set up persistent storage directory
    persist_dir = "chroma_db"
    os.makedirs(persist_dir, exist_ok=True)

    # File upload - allow multiple files
    uploaded_files = st.file_uploader(
        "Upload your documents",
        type=["pdf", "txt", "md", "markdown"],
        accept_multiple_files=True,
        help="Upload PDF, TXT, or Markdown files"
    )

    if uploaded_files:
        # Display uploaded files
        st.sidebar.write("Uploaded files:")
        for file in uploaded_files:
            st.sidebar.write(f"- {file.name}")
            
        # Process documents
        if "qa_chain" not in st.session_state:
            with st.spinner("Processing documents..."):
                try:
                    text = load_documents(uploaded_files)
                    if not text.strip():
                        st.error("No text could be extracted from the uploaded documents.")
                        return
                    
                    qa_chain = setup_rag_chain(text, persist_dir, ollama_base_url)
                    st.session_state["qa_chain"] = qa_chain
                    st.success("Documents processed! You can now ask questions.")
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")
                    return

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
                
                try:
                    response = st.session_state["qa_chain"].run(
                        query,
                        callbacks=[stream_handler]
                    )
                    
                    # Add assistant's response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
        else:
            st.warning("Please upload documents first.")

if __name__ == "__main__":
    main()