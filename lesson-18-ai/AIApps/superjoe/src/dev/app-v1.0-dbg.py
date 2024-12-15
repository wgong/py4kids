"""
Simple Semantic Similarity App
----------------------------
A streamlit app for exploring semantic similarity across languages.

Requirements:
    pip install streamlit sentence-transformers deep-translator numpy
"""

import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from deep_translator import GoogleTranslator

# Constants
LANGUAGES = {
    'English': 'en',
    'Chinese': 'zh-CN',
    'Spanish': 'es',
    'French': 'fr',
    'Japanese': 'ja'
}

def compute_cosine_similarity(v1, v2):
    """Compute cosine similarity between two vectors"""
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    return dot_product / (norm1 * norm2)

def get_similarity_display(score):
    """Create visual representation of similarity score"""
    stars = int(score * 10)
    return "⭐" * stars + "☆" * (10 - stars)

def main():
    st.set_page_config(page_title="Language Similarity", page_icon="🌍")
    
    st.title("🌍 Language Explorer")
    st.markdown("""
    Discover how words and phrases connect across different languages!
    Enter text in two different languages to see how similar they are in meaning.
    """)

    # Load model
    @st.cache_resource
    def load_model():
        return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    model = load_model()

    # Language selection
    col1, col2 = st.columns(2)
    with col1:
        lang1 = st.selectbox("First Language", options=list(LANGUAGES.keys()), key='lang1')
        text1 = st.text_area("Enter text", height=100, key='text1')
        
    with col2:
        lang2 = st.selectbox("Second Language", options=list(LANGUAGES.keys()), key='lang2')
        text2 = st.text_area("Enter text", height=100, key='text2')

    # Show translations if requested
    if st.checkbox("Show translations"):
        try:
            if text1:
                translation1 = GoogleTranslator(
                    source=LANGUAGES[lang1],
                    target=LANGUAGES[lang2]
                ).translate(text1)
                st.info(f"{lang1} → {lang2}: {translation1}")
            
            if text2:
                translation2 = GoogleTranslator(
                    source=LANGUAGES[lang2],
                    target=LANGUAGES[lang1]
                ).translate(text2)
                st.info(f"{lang2} → {lang1}: {translation2}")
        except Exception as e:
            st.warning("Translation error. Please try again with different text.")

    # Calculate similarity
    if text1 and text2:
        try:
            # Get embeddings
            embedding1 = model.encode(text1)
            embedding2 = model.encode(text2)
            
            # Calculate similarity
            similarity = compute_cosine_similarity(embedding1, embedding2)
            
            # Display results
            st.header("Results! 🎉")
            st.write(f"Similarity Score: {similarity:.2f}")
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
            st.error(f"Error processing text. Please try again. Error: {str(e)}")

    # Help section
    with st.expander("How does this work? 🤓"):
        st.markdown("""
        This app uses AI to understand languages! Here's what's happening:
        
        1. Your text gets converted into numbers (vectors) that capture its meaning
        2. We compare these vectors to see how similar they are
        3. More stars ⭐ means more similar meaning!
        
        Try these experiments:
        * Type the same word in different languages
        * Try similar but not identical concepts
        * Compare opposite words
        * Mix emoji with words
        """)

if __name__ == "__main__":
    main()