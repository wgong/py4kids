"""
Enhanced Language Explorer App
----------------------------
A streamlit app with improved error handling and interactivity.

Requirements:
    pip install streamlit sentence-transformers deep-translator numpy
"""

import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from deep_translator import GoogleTranslator
import socket
from typing import Optional, Tuple, Dict

# Constants
LANGUAGES = {
    'English': 'en',
    'Chinese': 'zh-CN',
    'Spanish': 'es',
    'French': 'fr',
    'Japanese': 'ja'
}

# Incompatible language pairs (if any)
INCOMPATIBLE_PAIRS = set([
    # Add any known incompatible language pairs here
    # ('lang1', 'lang2')
])

def check_internet() -> bool:
    """Check if internet connection is available"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def compute_cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Compute cosine similarity between two vectors"""
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    return dot_product / (norm1 * norm2)

def get_similarity_display(score: float) -> str:
    """Create visual representation of similarity score"""
    stars = int(score * 10)
    return "⭐" * stars + "☆" * (10 - stars)

def translate_text(text: str, source_lang: str, target_lang: str) -> Optional[str]:
    """Translate text with error handling"""
    if not check_internet():
        st.warning("⚠️ Translation requires internet connection. Please check your connectivity.")
        return None
    
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        result = translator.translate(text)
        if not result:
            st.warning(f"⚠️ Could not translate from {source_lang} to {target_lang}")
            return None
        return result
    except Exception as e:
        st.warning(f"⚠️ Translation error: {str(e)}")
        return None

def validate_input(text1: str, text2: str, lang1: str, lang2: str) -> bool:
    """Validate user input"""
    if not text1 or not text2:
        st.warning("⚠️ Please enter text in both languages")
        return False
    
    if lang1 == lang2:
        st.warning("⚠️ Please select different languages")
        return False
    
    if (lang1, lang2) in INCOMPATIBLE_PAIRS:
        st.warning("⚠️ This language combination is not supported")
        return False
    
    return True

def get_model_status() -> Tuple[bool, str]:
    """Check model status and return appropriate message"""
    try:
        load_model()
        return True, "✅ Model loaded successfully"
    except Exception as e:
        return False, f"❌ Error loading model: {str(e)}"

@st.cache_resource
def load_model():
    """Load the model with proper error handling"""
    try:
        return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        raise e

def main():
    st.set_page_config(page_title="Language Explorer", page_icon="🌍")
    
    # Title and description
    st.title("🌍 Language Explorer")
    st.markdown("""
    Discover how words and phrases connect across different languages! 
    Enter text in two different languages to see how similar they are in meaning.
    """)

    # Check and display model status in sidebar
    model_ok, model_message = get_model_status()
    st.sidebar.write("Model Status:", model_message)

    # Display network status
    is_online = check_internet()
    network_status = "🌐 Online" if is_online else "📴 Offline"
    st.sidebar.write("Network Status:", network_status)

    if model_ok:
        model = load_model()
        
        # Language selection
        col1, col2 = st.columns(2)
        with col1:
            lang1 = st.selectbox("First Language", options=list(LANGUAGES.keys()), key='lang1')
            text1 = st.text_area("Enter text", height=100, key='text1')
            
        with col2:
            lang2 = st.selectbox("Second Language", options=list(LANGUAGES.keys()), key='lang2')
            text2 = st.text_area("Enter text", height=100, key='text2')

        # Show translations if requested and online
        if st.checkbox("Show translations"):
            if is_online:
                if text1:
                    translation1 = translate_text(text1, LANGUAGES[lang1], LANGUAGES[lang2])
                    if translation1:
                        st.info(f"{lang1} → {lang2}: {translation1}")
                
                if text2:
                    translation2 = translate_text(text2, LANGUAGES[lang2], LANGUAGES[lang1])
                    if translation2:
                        st.info(f"{lang2} → {lang1}: {translation2}")
            else:
                st.warning("⚠️ Translations require internet connection")

        # Calculate similarity when both inputs are valid
        if text1 and text2 and validate_input(text1, text2, lang1, lang2):
            try:
                with st.spinner("Calculating similarity..."):
                    # Get embeddings
                    embedding1 = model.encode(text1)
                    embedding2 = model.encode(text2)
                    
                    # Calculate similarity
                    similarity = compute_cosine_similarity(embedding1, embedding2)
                    
                    # Create result container
                    result_container = st.container()
                    with result_container:
                        st.header("Results! 🎉")
                        
                        # Display similarity metrics
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Similarity Score", f"{similarity:.2f}")
                        with col2:
                            st.write("Visual Similarity:", get_similarity_display(similarity))
                        
                        # Fun feedback
                        if similarity > 0.8:
                            st.balloons()
                            st.success("WOW! These are very similar! 🎯")
                        elif similarity > 0.6:
                            st.success("Pretty close! 👍")
                        elif similarity > 0.4:
                            st.info("Somewhat similar! 🤔")
                        else:
                            st.warning("These seem quite different! 🌈")
                    
            except Exception as e:
                st.error(f"Error processing text: {str(e)}")
                st.error("Please try again with different text")

    # Help section
    with st.expander("How does this work? 🤓"):
        st.markdown("""
        This app uses AI to understand languages! Here's what's happening:
        
        1. Your text gets converted into numbers (vectors) that capture its meaning
        2. We compare these vectors to see how similar they are
        3. More stars ⭐ means more similar meaning!
        
        **Tips:**
        * Make sure you're online for translations
        * Enter text in both languages
        * Try simple phrases first
        
        **Fun experiments to try:**
        * Same word in different languages
        * Similar but not identical concepts
        * Opposite words
        * Mix emoji with words
        """)

if __name__ == "__main__":
    main()