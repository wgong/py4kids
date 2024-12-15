"""
Language Explorer with Semantic Comparison
---------------------------------------
A streamlit app that explores semantic relationships across languages.

Requirements:
    pip install streamlit sentence-transformers deep-translator numpy pandas plotly
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs
from sentence_transformers import SentenceTransformer
from deep_translator import GoogleTranslator
import socket
from typing import Optional, Tuple, Dict, List
from pathlib import Path

# Constants
LANGUAGES = {
    'English': 'en',
    'Chinese': 'zh-CN',
    'Spanish': 'es',
    'French': 'fr',
    'Japanese': 'ja'
}

# Semantic examples for each language
SEMANTIC_EXAMPLES = {
    'English': ['dog', 'cat', 'pet', 'animal', 'friend', 'companion'],
    'Chinese': ['狗', '猫', '宠物', '动物', '朋友', '伙伴'],
    'Spanish': ['perro', 'gato', 'mascota', 'animal', 'amigo', 'compañero'],
    'French': ['chien', 'chat', 'animal de compagnie', 'animal', 'ami', 'compagnon'],
    'Japanese': ['犬', '猫', 'ペット', '動物', '友達', '仲間']
}

# Incompatible language pairs (if any)
INCOMPATIBLE_PAIRS = set([
    # Add any known incompatible language pairs here
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
        st.warning("⚠️ Translation requires internet connection")
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

def get_semantic_field(text: str, lang: str, model: SentenceTransformer) -> List[Tuple[str, float]]:
    """Get semantic field (related words) for given text"""
    examples = SEMANTIC_EXAMPLES[lang]
    text_embedding = model.encode(text)
    
    similarities = []
    for example in examples:
        example_embedding = model.encode(example)
        similarity = compute_cosine_similarity(text_embedding, example_embedding)
        similarities.append((example, similarity))
    
    return sorted(similarities, key=lambda x: x[1], reverse=True)

def plot_semantic_comparison(similarities1: List[Tuple[str, float]], 
                           similarities2: List[Tuple[str, float]],
                           lang1: str, lang2: str) -> plotly.graph_objs.Figure:
    """Create a comparison plot of semantic similarities"""
    df = pd.DataFrame({
        f'{lang1} Similarities': [s[1] for s in similarities1],
        f'{lang2} Similarities': [s[1] for s in similarities2],
        'Words': [f'{s1[0]}/{s2[0]}' for s1, s2 in zip(similarities1, similarities2)]
    })
    
    fig = px.bar(df, x='Words', y=[f'{lang1} Similarities', f'{lang2} Similarities'],
                 title='Semantic Field Comparison',
                 barmode='group',
                 color_discrete_sequence=['#FF4B4B', '#0068C9'])
    
    fig.update_layout(
        xaxis_title="Related Word Pairs",
        yaxis_title="Semantic Similarity",
        height=400
    )
    
    return fig

def main():
    st.set_page_config(page_title="Language Explorer", page_icon="🌍", layout="wide")
    
    st.title("🌍 Language Explorer")
    st.markdown("""
    Explore semantic relationships across languages! See how words and concepts
    connect and compare their semantic fields.
    """)

    # Model loading and status checks
    model_ok, model_message = get_model_status()
    st.sidebar.write("Model Status:", model_message)
    is_online = check_internet()
    st.sidebar.write("Network Status:", "🌐 Online" if is_online else "📴 Offline")
    
    if model_ok:
        model = load_model()
        
        # Language selection and text input
        col1, col2 = st.columns(2)
        with col1:
            lang1 = st.selectbox("First Language", options=list(LANGUAGES.keys()), key='lang1')
            text1 = st.text_area("Enter text", height=100, key='text1')
            
        with col2:
            lang2 = st.selectbox("Second Language", options=list(LANGUAGES.keys()), key='lang2')
            text2 = st.text_area("Enter text", height=100, key='text2')

        # Show translations if requested
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
        
        # Semantic Comparison Section
        if text1 and text2 and validate_input(text1, text2, lang1, lang2):
            try:
                with st.spinner("Analyzing semantic relationships..."):
                    # Get embeddings and basic similarity
                    embedding1 = model.encode(text1)
                    embedding2 = model.encode(text2)
                    similarity = compute_cosine_similarity(embedding1, embedding2)
                    
                    # Calculate semantic fields
                    semantic_field1 = get_semantic_field(text1, lang1, model)
                    semantic_field2 = get_semantic_field(text2, lang2, model)
                    
                    # Display results
                    st.header("Semantic Analysis Results 🎯")
                    
                    # Basic similarity score
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        st.metric("Direct Similarity", f"{similarity:.2f}")
                    with col2:
                        st.write("Visual Match:", get_similarity_display(similarity))
                    with col3:
                        if similarity > 0.8:
                            st.success("Excellent match! 🎯")
                        elif similarity > 0.6:
                            st.success("Good match! 👍")
                        elif similarity > 0.4:
                            st.info("Partial match 🤔")
                        else:
                            st.warning("Different meanings 🌈")
                    
                    # Semantic field comparison
                    st.subheader("Semantic Field Analysis 🔍")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Related words in {lang1}:**")
                        for word, sim in semantic_field1[:5]:
                            st.write(f"- {word}: {sim:.2f} {get_similarity_display(sim)}")
                            
                    with col2:
                        st.write(f"**Related words in {lang2}:**")
                        for word, sim in semantic_field2[:5]:
                            st.write(f"- {word}: {sim:.2f} {get_similarity_display(sim)}")
                    
                    # Visualization
                    st.subheader("Semantic Field Comparison 📊")
                    fig = plot_semantic_comparison(
                        semantic_field1, semantic_field2, lang1, lang2)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Insights
                    st.subheader("Semantic Insights 💡")
                    with st.expander("See detailed analysis"):
                        st.write("""
                        This analysis shows how your words relate to other concepts in each language.
                        Here's what the results mean:
                        
                        1. **Direct Similarity**: How closely the meanings match
                        2. **Semantic Field**: Related words and concepts
                        3. **Comparison**: How the words relate to similar concepts
                        """)
                        
                        if similarity > 0.8:
                            st.success("""
                            These words/phrases are very close in meaning! They likely:
                            - Share the same core concept
                            - Are used in similar contexts
                            - Have similar cultural connotations
                            """)
                        elif similarity > 0.6:
                            st.info("""
                            These words/phrases are related but might:
                            - Have slight differences in usage
                            - Carry different cultural nuances
                            - Be used in somewhat different contexts
                            """)
                        else:
                            st.warning("""
                            These words/phrases show significant differences:
                            - They might be used differently
                            - Could have different cultural meanings
                            - Might belong to different semantic fields
                            """)
                    
            except Exception as e:
                st.error(f"Error in semantic analysis: {str(e)}")
                st.error("Please try again with different text")

    # Help section
    with st.expander("How does this work? 🤓"):
        st.markdown("""
        This app uses AI to analyze and compare word meanings across languages:
        
        1. **Direct Comparison**: Measures how similar two words/phrases are
        2. **Semantic Field**: Shows related words in each language
        3. **Visual Analysis**: Graphs showing how meanings compare
        
        **Tips for best results:**
        * Start with simple words or short phrases
        * Try comparing:
            - Direct translations
            - Similar concepts
            - Cultural equivalents
        * Look at the semantic field to understand usage
        
        **Fun experiments:**
        * Compare idioms across languages
        * Look at cultural concepts
        * Compare formal vs informal expressions
        """)

if __name__ == "__main__":
    main()