"""
Semantic Analyzer Page
-------------------
Semantic analysis functionality with multiple embedding model support and flexible context probes.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict
from utils.language_utils import LANGUAGES, SEMANTIC_CONTEXT, EXAMPLE_PAIRS

import os
os.environ["HUGGINGFACE_TOKEN"] = os.getenv("HUGGING_FACE_API_KEY")

EMBEDDING_MODELS = {
    'Word Level Models': {
        'Multilingual MiniLM': 'paraphrase-multilingual-MiniLM-L12-v2',
        'MPNet': 'all-mpnet-base-v2',
        'BGE Large': 'bge-large-en-v1.5',
        'Multilingual E5': 'multilingual-e5-large',
        'E5 Large': 'e5-large-v2'
    },
    'Text Level Models': {
        'MiniLM': 'all-MiniLM-L6-v2',
        'MPNet Base': 'all-mpnet-base-v2',
        'E5 Large': 'e5-large-v2',
        'BGE Large': 'bge-large-en-v1.5'
    }
}

DEFAULT_PROBES = [
    "nature and environment",
    "technology and innovation",
    "culture and society",
    "business and economy",
    "science and education",
    "art and creativity",
    "health and wellbeing",
    "politics and governance",
    "philosophy and thought",
    "daily life and activities"
]

PROBE_TEMPLATES = [
    "This text is about {}",
    "This content relates to {}",
    "This discusses {}",
    "This focuses on {}"
]

@st.cache_resource
def load_model(model_path: str) -> SentenceTransformer:
    """Load a specific embedding model"""
    return SentenceTransformer(model_path)

def compute_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Compute cosine similarity between two vectors"""
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    return dot_product / (norm1 * norm2)

def get_similarity_display(score: float) -> str:
    """Create visual representation of similarity score"""
    stars = int(score * 10)
    return "⭐" * stars + "☆" * (10 - stars)

def get_semantic_category(text: str, model: SentenceTransformer) -> str:
    """Dynamically determine the semantic category of the input text"""
    probes = {
        'animal': 'animal pet creature',
        'human': 'human person people',
        'object': 'thing object item'
    }
    
    text_embedding = model.encode(text)
    similarities = {}
    
    for category, probe in probes.items():
        probe_embedding = model.encode(probe)
        similarity = compute_similarity(text_embedding, probe_embedding)
        similarities[category] = similarity
    
    return max(similarities.items(), key=lambda x: x[1])[0]

def get_semantic_field(text: str, lang: str, model: SentenceTransformer, 
                      is_text_level: bool, custom_probes: List[str] = None) -> List[Tuple[str, float]]:
    """Get semantic field (related words/concepts) for given text with flexible context probes"""
    if is_text_level:
        # Use custom probes if provided, otherwise use defaults
        probes = custom_probes if custom_probes else DEFAULT_PROBES
        
        text_embedding = model.encode(text)
        similarities = []
        
        for probe in probes:
            # Try different templates and take max similarity
            probe_similarities = []
            for template in PROBE_TEMPLATES:
                formatted_probe = template.format(probe)
                probe_embedding = model.encode(formatted_probe)
                sim = compute_similarity(text_embedding, probe_embedding)
                probe_similarities.append(sim)
            
            # Take the highest similarity across templates
            max_sim = max(probe_similarities)
            similarities.append((probe, max_sim))
    else:
        # Use existing word-level analysis
        category = get_semantic_category(text, model)
        context_words = SEMANTIC_CONTEXT[category][lang]
        
        text_embedding = model.encode(text)
        similarities = []
        
        for word in context_words:
            word_embedding = model.encode(word)
            similarity = compute_similarity(text_embedding, word_embedding)
            similarities.append((word, similarity))
    
    return sorted(similarities, key=lambda x: x[1], reverse=True)

def plot_semantic_comparison(similarities1: List[Tuple[str, float]], 
                           similarities2: List[Tuple[str, float]],
                           label1: str, label2: str) -> plotly.graph_objs.Figure:
    """Create a comparison plot of semantic similarities"""
    df = pd.DataFrame({
        f'{label1}': [s[1] for s in similarities1],
        f'{label2}': [s[1] for s in similarities2],
        'Concepts': [f'{s1[0]}/{s2[0]}' for s1, s2 in zip(similarities1, similarities2)]
    })
    
    fig = px.bar(df, x='Concepts', y=[f'{label1}', f'{label2}'],
                 title='Semantic Field Comparison',
                 barmode='group',
                 color_discrete_sequence=['#FF4B4B', '#0068C9'])
    
    fig.update_layout(
        xaxis_title="Concept Pairs",
        yaxis_title="Semantic Similarity",
        height=400
    )
    return fig

def show_semantic_analyzer():
    st.title("🎯 Semantic Analyzer")
    st.markdown("""
    Explore how different words and concepts relate to each other! This tool analyzes the semantic 
    relationships between words or texts and shows their related concepts and meanings.
    """)

    # Model selection
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_level = st.selectbox(
            "Select Analysis Level",
            options=list(EMBEDDING_MODELS.keys()),
            help="Choose between word-level or text-level analysis"
        )
    
    with col2:
        model_name = st.selectbox(
            "Select Embedding Model",
            options=list(EMBEDDING_MODELS[analysis_level].keys()),
            help="Choose the specific embedding model to use"
        )

    # Load selected model
    model_path = EMBEDDING_MODELS[analysis_level][model_name]
    model = load_model(model_path)
    is_text_level = analysis_level == 'Text Level Models'

    # Model information
    with st.expander("ℹ️ Model Information"):
        st.markdown(f"""
        **Selected Model:** {model_name}  
        **Model Path:** {model_path}  
        **Analysis Level:** {analysis_level}  
        
        This model is optimized for {analysis_level.lower()} analysis. Experiment with different models
        to see how they interpret and relate concepts differently!
        """)

    # Context probe customization
    custom_probes = None
    if is_text_level:
        with st.expander("🎯 Customize Context Probes"):
            st.markdown("""
            Add your own context probes for analysis. Enter one probe per line.
            Example: 
            - personal emotions
            - historical events
            - scientific concepts
            """)
            custom_probes_text = st.text_area(
                "Custom Context Probes",
                height=150,
                help="Enter your custom probes, one per line. Leave empty to use default probes.",
                key="custom_probes"
            )
            
            if custom_probes_text.strip():
                custom_probes = [p.strip() for p in custom_probes_text.split('\n') if p.strip()]

    # Input fields with appropriate labels
    col1, col2 = st.columns(2)
    with col1:
        text1 = st.text_area(
            "Enter first " + ("text" if is_text_level else "word/concept"), 
            height=100, 
            key='text1',
            placeholder="Enter " + ("a short text" if is_text_level else "a word or concept")
        )
        
    with col2:
        text2 = st.text_area(
            "Enter second " + ("text" if is_text_level else "word/concept"), 
            height=100, 
            key='text2',
            placeholder="Enter " + ("another text" if is_text_level else "another word or concept")
        )

    # Analysis button
    if st.button("🔍 Analyze Semantic Relationship"):
        if text1 and text2:
            with st.spinner(f"Analyzing semantic relationships using {model_name}..."):
                try:
                    # Get embeddings and calculate similarity
                    embed1 = model.encode(text1)
                    embed2 = model.encode(text2)
                    similarity = compute_similarity(embed1, embed2)
                    
                    # Get semantic fields with custom probes
                    field1 = get_semantic_field(text1, 'English', model, is_text_level, custom_probes)
                    field2 = get_semantic_field(text2, 'English', model, is_text_level, custom_probes)
                    
                    # Display results
                    st.header("Analysis Results")
                    
                    # Basic similarity metrics
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        st.metric("Similarity Score", f"{similarity:.2f}")
                    with col2:
                        st.write("Match Level:", get_similarity_display(similarity))
                    with col3:
                        if similarity > 0.8:
                            st.success("Strong match! 🎯")
                        elif similarity > 0.6:
                            st.success("Good match! 👍")
                        elif similarity > 0.4:
                            st.info("Partial match 🤔")
                        else:
                            st.warning("Weak match 🌈")

                    # Semantic fields
                    st.subheader("Semantic Analysis")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**First {('text' if is_text_level else 'word')} semantic field:**")
                        for concept, sim in field1[:5]:
                            st.write(f"- {concept}: {sim:.2f} {get_similarity_display(sim)}")
                    with col2:
                        st.write(f"**Second {('text' if is_text_level else 'word')} semantic field:**")
                        for concept, sim in field2[:5]:
                            st.write(f"- {concept}: {sim:.2f} {get_similarity_display(sim)}")

                    # Visualization
                    st.subheader("Comparative Analysis")
                    fig = plot_semantic_comparison(
                        field1, field2, 
                        "First " + ("Text" if is_text_level else "Word"),
                        "Second " + ("Text" if is_text_level else "Word")
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Interpretation
                    with st.expander("📊 Interpretation Guide"):
                        st.markdown(f"""
                        **Similarity Score: {similarity:.2f}**
                        
                        This analysis using {model_name} shows:
                        1. **Direct Match:** {get_similarity_display(similarity)}
                        2. **Semantic Field Overlap:** How related concepts compare
                        3. **Analysis Level:** {analysis_level} analysis showing 
                           {'thematic relationships' if is_text_level else 'conceptual relationships'}
                        
                        {
                        "Strong match! The inputs share very similar semantic spaces and themes." 
                        if similarity > 0.8 else 
                        "Good match! The inputs are related but might have subtle differences in meaning or context." 
                        if similarity > 0.6 else 
                        "Partial match. The inputs share some semantic elements but differ in key aspects." 
                        if similarity > 0.4 else 
                        "The inputs show significant differences in meaning or thematic content."
                        }
                        """)
                except Exception as e:
                    st.error(f"Error in analysis: {str(e)}")
                    st.error("Please try different input or check your text")

def main():
    st.set_page_config(page_title="Semantic Analyzer", page_icon="🎯", layout="wide")
    show_semantic_analyzer()

if __name__ == "__main__":
    main()