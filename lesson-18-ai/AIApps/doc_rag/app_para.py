from langchain.text_splitter import TextSplitter
from typing import List
import re

class ParagraphTextSplitter(TextSplitter):
    """Split text based on paragraphs while respecting natural boundaries"""
    
    def __init__(
        self,
        separator: str = "\n\n",
        min_paragraph_length: int = 50,
        max_paragraph_length: int = 1500,
        cleanup_regex: str = r'\s+',
        **kwargs
    ):
        """Initialize the paragraph splitter.
        
        Args:
            separator: String to split paragraphs on (default: double newline)
            min_paragraph_length: Minimum length for a paragraph to be kept
            max_paragraph_length: Maximum length for a paragraph before forcing a split
            cleanup_regex: Regex pattern for cleaning up whitespace
        """
        super().__init__(**kwargs)
        self.separator = separator
        self.min_paragraph_length = min_paragraph_length
        self.max_paragraph_length = max_paragraph_length
        self.cleanup_regex = cleanup_regex
    
    def split_text(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        # Clean up whitespace
        text = re.sub(self.cleanup_regex, ' ', text)
        
        # Split into initial paragraphs
        paragraphs = text.split(self.separator)
        
        # Process and filter paragraphs
        processed_chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            
            # Skip if paragraph is too short
            if len(paragraph) < self.min_paragraph_length:
                if current_chunk:
                    current_chunk += " " + paragraph
                else:
                    current_chunk = paragraph
                continue
            
            # If paragraph is too long, split it further
            if len(paragraph) > self.max_paragraph_length:
                # First, add any existing current_chunk
                if current_chunk:
                    processed_chunks.append(current_chunk)
                    current_chunk = ""
                
                # Split long paragraph into sentences
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                temp_chunk = ""
                
                for sentence in sentences:
                    if len(temp_chunk) + len(sentence) > self.max_paragraph_length:
                        if temp_chunk:
                            processed_chunks.append(temp_chunk.strip())
                        temp_chunk = sentence
                    else:
                        temp_chunk += " " + sentence if temp_chunk else sentence
                
                if temp_chunk:
                    processed_chunks.append(temp_chunk.strip())
            else:
                # Regular paragraph
                if current_chunk:
                    if len(current_chunk) + len(paragraph) > self.max_paragraph_length:
                        processed_chunks.append(current_chunk)
                        current_chunk = paragraph
                    else:
                        current_chunk += " " + paragraph
                else:
                    current_chunk = paragraph
        
        # Add any remaining chunk
        if current_chunk:
            processed_chunks.append(current_chunk)
        
        # Final cleanup and filtering
        return [chunk.strip() for chunk in processed_chunks 
                if len(chunk.strip()) >= self.min_paragraph_length]

# Example usage in the RAG application:
def setup_rag_chain(text: str, collection_name: str, ollama_base_url: str = "http://localhost:11434"):
    embeddings = OllamaEmbeddings(
        model="llama2", 
        base_url=ollama_base_url
    )
    
    # Use paragraph-based splitting instead of RecursiveCharacterTextSplitter
    text_splitter = ParagraphTextSplitter(
        min_paragraph_length=100,  # Minimum meaningful paragraph
        max_paragraph_length=1000,  # Maximum chunk size
        separator="\n\n"           # Split on double newlines
    )
    
    chunks = text_splitter.split_text(text)
    
    # Rest of the function remains the same...