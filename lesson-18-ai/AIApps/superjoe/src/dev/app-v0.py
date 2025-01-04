"""
Network-Aware Multilingual Semantic Game
--------------------------------------
A Streamlit app that works both online and offline for language learning!

Installation:
    pip install streamlit transformers torch deep-translator scipy requests sentence-transformers

Usage:
    streamlit run semantic_game.py
"""

import streamlit as st
import torch
from scipy.spatial.cosine import cosine
from deep_translator import GoogleTranslator
import emoji
import requests
from pathlib import Path
import os
from sentence_transformers import SentenceTransformer
import socket
from typing import Dict, Optional, Any, Tuple

# Constants
LANGUAGES = {
    'English': 'en',
    'Chinese': 'zh-CN',
    'Spanish': 'es',
    'French': 'fr',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Russian': 'ru',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'German': 'de'
}

class NetworkAwareTranslator:
    """Handles translations with network awareness"""
    
    def __init__(self):
        self.is_online = self._check_internet()

    @staticmethod
    def _check_internet() -> bool:
        """Check internet connectivity"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate text with network awareness"""
        if not self.is_online:
            st.warning("⚠️ Translation requires internet connection")
            return None
        
        try:
            return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        except Exception as e:
            st.error(f"Translation error: {str(e)}")
            return None

class ModelManager:
    """Manages model loading and embedding generation"""
    
    def __init__(self):
        self.model_info = self._load_model()

    @staticmethod
    @st.cache_resource
    def _load_model() -> Optional[Dict[str, Any]]:
        """Load appropriate model based on network availability"""
        is_online = NetworkAwareTranslator._check_internet()
        
        if is_online:
            st.sidebar.success("🌐 Online mode: Using full features!")
            try:
                from transformers import XLMRobertaTokenizer, XLMRobertaModel
                tokenizer = XLMRobertaTokenizer.from_pretrained('xlm-roberta-base')
                model = XLMRobertaModel.from_pretrained('xlm-roberta-base')
                return {'type': 'online', 'model': model, 'tokenizer': tokenizer}
            except Exception:
                st.sidebar.warning("⚠️ Failed to load online model, falling back to offline mode")
                is_online = False
        
        st.sidebar.info("📱 Offline mode: Using local model")
        if ModelManager._ensure_offline_model():
            model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            return {'type': 'offline', 'model': model}
        return None

    @staticmethod
    def _ensure_offline_model() -> bool:
        """Ensure offline model is downloaded"""
        model_name = 'paraphrase-multilingual-MiniLM-L12-v2'
        cache_dir = Path.home() / '.cache' / 'torch' / 'sentence_transformers'
        if not (cache_dir / model_name).exists():
            st.warning("""
            🌐 Offline model not found! Please connect to the internet once to download it:
            ```python
            from sentence_transformers import SentenceTransformer
            SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            ```
            """)
            return False
        return True

    def get_embedding(self, text: str) -> Optional[torch.Tensor]:
        """Generate embeddings using appropriate model"""
        if not self.model_info:
            return None
            
        if self.model_info['type'] == 'online':
            inputs = self.model_info['tokenizer'](
                text, 
                return_tensors='pt', 
                padding=True, 
                truncation=True, 
                max_length=512
            )
            with torch.no_grad():
                outputs = self.model_info['model'](**inputs)
            return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        else:
            return self.model_info['model'].encode(text)

class SimilarityAnalyzer:
    """Handles similarity calculations and visualization"""
    
    @staticmethod
    def calculate_similarity(embed1: torch.Tensor, embed2: torch.Tensor) -> float:
        """Calculate cosine similarity between embeddings"""
        return 1 - cosine(embed1, embed2)

    @staticmethod
    def get_similarity_display(score: float) -> str:
        """Create visual representation of similarity"""
        stars = int(score * 10)
        return "⭐" * stars + "☆" * (10 - stars)

    @staticmethod
    def get_feedback(similarity: float) -> Tuple[str, str]:
        """Get appropriate feedback based on similarity score"""
        if similarity > 0.8:
            return "WOW! These are very similar! 🎯", "success"
        elif similarity > 0.6:
            return "Pretty close! 👍", "success"
        elif similarity > 0.4:
            return "Somewhat similar! 🤔", "info"
        else:
            return "These seem quite different! 🌈", "warning"

def setup_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Language Similarity Game!",
        page_icon="🌍",
        initial_sidebar_state="expanded"
    )

def render_ui() -> Tuple[str, str, str, str]:
    """Render UI elements and return user inputs"""
    st.title("🌍 Language Similarity Game! 🎮")
    st.markdown("""
    Explore how words and phrases are similar across different languages! 
    This app works both online and offline - perfect for learning anywhere!
    """)

    # Language selection
    st.sidebar.header("Choose Languages 🗣")
    lang1 = st.sidebar.selectbox("Select First Language", list(LANGUAGES.keys()), index=0)
    lang2 = st.sidebar.selectbox("Select Second Language", list(LANGUAGES.keys()), index=1)

    # Text input
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Enter text in {lang1}")
        text1 = st.text_area("Text 1", height=100, key="text1")
    with col2:
        st.subheader(f"Enter text in {lang2}")
        text2 = st.text_area("Text 2", height=100, key="text2")

    return lang1, lang2, text1, text2

def render_help_sections():
    """Render help and instructions sections"""
    with st.expander("How does this work? 🤓"):
        st.markdown("""
        This game uses AI to understand languages! It works in two modes:

        🌐 **Online Mode**
        - Uses a powerful AI model
        - Provides translations
        - More accurate similarity scores

        📱 **Offline Mode**
        - Uses a smaller, downloaded model
        - Works without internet
        - Perfect for learning on the go!
        """)

    with st.expander("First-time Setup Instructions 📥"):
        st.markdown("""
        To use this app offline:

        1. First, run with internet connection to download models:
        ```python
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        ```

        2. The model will be saved locally (about 120MB)
        3. You can then use the app offline!
        """)

def main():
    """Main application logic"""
    setup_page()
    
    # Initialize components
    translator = NetworkAwareTranslator()
    model_manager = ModelManager()
    similarity_analyzer = SimilarityAnalyzer()

    if not model_manager.model_info:
        st.error("Please connect to internet once to download the required model.")
        st.stop()

    # Render UI and get inputs
    lang1, lang2, text1, text2 = render_ui()

    # Handle translations if online
    if translator.is_online and st.checkbox("Show translations 🔄"):
        if text1:
            translation1 = translator.translate(text1, LANGUAGES[lang1], LANGUAGES[lang2])
            if translation1:
                st.info(f"{lang1} → {lang2}: {translation1}")
        if text2:
            translation2 = translator.translate(text2, LANGUAGES[lang2], LANGUAGES[lang1])
            if translation2:
                st.info(f"{lang2} → {lang1}: {translation2}")

    # Calculate and display similarity
    if text1 and text2:
        try:
            embed1 = model_manager.get_embedding(text1)
            embed2 = model_manager.get_embedding(text2)
            
            if embed1 is not None and embed2 is not None:
                similarity = similarity_analyzer.calculate_similarity(embed1, embed2)
                
                st.header("Results! 🎉")
                st.write(f"Similarity Score: {similarity:.2f}")
                st.write("Visual Similarity:", similarity_analyzer.get_similarity_display(similarity))
                
                feedback, level = similarity_analyzer.get_feedback(similarity)
                if similarity > 0.8:
                    st.balloons()
                getattr(st, level)(feedback)
                
        except Exception as e:
            st.error(f"Error processing text: {str(e)}")

    render_help_sections()

if __name__ == "__main__":
    main()