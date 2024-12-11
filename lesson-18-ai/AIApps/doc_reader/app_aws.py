import streamlit as st
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.llms.bedrock import Bedrock
from PyPDF2 import PdfReader
from typing import List, BinaryIO
import boto3
import os
import json

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

def get_collections():
    """Get list of existing collections"""
    collections_file = "collections.json"
    if os.path.exists(collections_file):
        with open(collections_file, 'r') as f:
            return json.load(f)
    return {}

def save_collections(collections):
    """Save collections metadata"""
    with open("collections.json", 'w') as f:
        json.dump(collections, f)

def setup_bedrock_client(region_name="us-east-1"):
    """Set up AWS Bedrock client"""
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=region_name
    )

def setup_rag_chain(text: str, collection_name: str, region_name: str = "us-east-1"):
    """Set up the RAG pipeline with document processing and Chroma vector storage"""
    # Initialize Bedrock client
    bedrock_client = setup_bedrock_client(region_name)
    
    # Initialize embeddings model (using Claude 3 Sonnet for embeddings)
    embeddings = BedrockEmbeddings(
        client=bedrock_client,
        model_id="anthropic.claude-3-sonnet-20240229-v1:0"
    )
    
    # Initialize LLM (Claude 3 Sonnet)
    llm = Bedrock(
        client=bedrock_client,
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={
            "temperature": 0.5,
            "max_tokens": 1000,
            "top_p": 0.9,
        }
    )

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Create persist directory for this collection
    persist_dir = os.path.join("chroma_db", collection_name)
    os.makedirs(persist_dir, exist_ok=True)

    # Create or load vector store
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    vectorstore.persist()  # Save the embeddings to disk

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    
    return qa_chain

def main():
    st.set_page_config(page_title="Chat with Document Collections", page_icon="📚")
    st.header("📚 Chat with your Document Collections")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # AWS Region configuration in sidebar
    aws_region = st.sidebar.text_input(
        "AWS Region",
        value="us-east-1",
        help="Enter your AWS region (e.g., us-east-1)"
    )

    # Collection management in sidebar
    st.sidebar.subheader("Collection Management")
    
    # Load existing collections
    collections = get_collections()
    
    # Create new collection
    new_collection = st.sidebar.text_input("Create new collection:")
    if st.sidebar.button("Create Collection") and new_collection:
        if new_collection not in collections:
            collections[new_collection] = {"files": []}
            save_collections(collections)
            st.sidebar.success(f"Collection '{new_collection}' created!")
        else:
            st.sidebar.error("Collection already exists!")

    # Select collection
    if collections:
        selected_collection = st.sidebar.selectbox(
            "Select Collection",
            options=list(collections.keys()),
            index=0
        )

        # Show files in collection
        if selected_collection:
            st.sidebar.write("Files in collection:")
            for file in collections[selected_collection]["files"]:
                st.sidebar.write(f"- {file}")

            # File upload for selected collection
            uploaded_files = st.file_uploader(
                f"Add documents to '{selected_collection}'",
                type=["pdf", "txt", "md", "markdown"],
                accept_multiple_files=True,
                help="Upload PDF, TXT, or Markdown files"
            )

            if uploaded_files:
                # Update collection with new files
                if st.button("Process Documents"):
                    with st.spinner("Processing documents..."):
                        try:
                            text = load_documents(uploaded_files)
                            if not text.strip():
                                st.error("No text could be extracted from the uploaded documents.")
                                return
                            
                            # Update collection metadata
                            new_files = [f.name for f in uploaded_files]
                            collections[selected_collection]["files"].extend(new_files)
                            save_collections(collections)
                            
                            # Process documents
                            qa_chain = setup_rag_chain(text, selected_collection, aws_region)
                            st.session_state["qa_chain"] = qa_chain
                            st.session_state["current_collection"] = selected_collection
                            st.success("Documents processed and added to collection!")
                        except Exception as e:
                            st.error(f"Error processing documents: {str(e)}")
                            return
    else:
        st.info("Create a collection to get started!")

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
            st.warning("Please select a collection and process documents first.")

if __name__ == "__main__":
    main()