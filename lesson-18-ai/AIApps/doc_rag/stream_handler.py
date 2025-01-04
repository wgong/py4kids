from langchain_core.callbacks import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    """Handler for streaming LLM responses to Streamlit"""
    
    def __init__(self, container, initial_text=""):
        """Initialize the handler with a container for displaying text."""
        self.container = container
        self.text = initial_text
        # Required for BaseCallbackHandler
        self.raise_error = False
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.text += token
        self.container.message(self.text, is_user=False)
    
    def on_llm_start(self, *args, **kwargs) -> None:
        """Run when LLM starts running."""
        pass
    
    def on_llm_end(self, *args, **kwargs) -> None:
        """Run when LLM ends running."""
        pass
    
    def on_llm_error(self, error: Exception, **kwargs) -> None:
        """Run when LLM errors."""
        pass
    
    def on_chain_start(self, *args, **kwargs) -> None:
        """Run when chain starts running."""
        pass
    
    def on_chain_end(self, *args, **kwargs) -> None:
        """Run when chain ends running."""
        pass
    
    def on_chain_error(self, error: Exception, **kwargs) -> None:
        """Run when chain errors."""
        pass
    
    def on_tool_start(self, *args, **kwargs) -> None:
        """Run when tool starts running."""
        pass
    
    def on_tool_end(self, *args, **kwargs) -> None:
        """Run when tool ends running."""
        pass
    
    def on_tool_error(self, error: Exception, **kwargs) -> None:
        """Run when tool errors."""
        pass