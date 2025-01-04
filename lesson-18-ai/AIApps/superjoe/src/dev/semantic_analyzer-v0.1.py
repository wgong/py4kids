"""
Semantic Comparison Tool
----------------------
A streamlit app for analyzing semantic relationships between languages.

Requirements:
    pip install streamlit sentence-transformers numpy pandas plotly
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict

# Constants
LANGUAGES = {
    'English': ['dog', 'cat', 'pet', 'animal', 'friend', 'companion'],
    'Chinese': ['狗', '猫', '宠物', '动物', '朋友', '伙伴'],
    'Spanish': ['perro', 'gato', 'mascota', 'animal', 'amigo', 'compañero'],
    'French': ['chien', 'chat', 'animal de compagnie', 'animal', 'ami', 'compagnon'],
    'Japanese': ['犬', '猫', 'ペット', '動物', '友達', '仲間']
}

EXAMPLE_PAIRS = {
    'Animals': {'English': 'dog', 'Chinese': '狗', 'Spanish': 'perro', 'French': 'chien', 'Japanese': '犬'},
    'Family': {'English': 'family', 'Chinese': '家庭', 'Spanish': 'familia', 'French': 'famille', 'Japanese': '家族'},
    'Love': {'English': 'love', 'Chinese': '爱', 'Spanish': 'amor', 'French': 'amour', 'Japanese': '愛'},
    'Happiness': {'English': 'happiness', 'Chinese': '幸福', 'Spanish': 'felicidad', 'French': 'bonheur', 'Japanese': '幸せ'}
}

@st.cache_resource
def load_model():
    """Load the multilingual model"""
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

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

def get_semantic_field(text: str, examples: List[str], model: SentenceTransformer) -> List[Tuple[str, float]]:
    """Get semantic field (related words) for given text"""
    text_embedding = model.encode(text)
    similarities = []
    for example in examples:
        example_embedding = model.encode(example)
        similarity = compute_similarity(text_embedding, example_embedding)
        similarities.append((example, similarity))
    return sorted(similarities, key=lambda x: x[1], reverse=True)

def plot_semantic_comparison(similarities1: List[Tuple[str, float]], 
                           similarities2: List[Tuple[str, float]],
                           lang1: str, lang2: str) -> plotly.graph_objs.Figure:
    """Create a comparison plot of semantic similarities"""
    df = pd.DataFrame({
        f'{lang1}': [s[1] for s in similarities1],
        f'{lang2}': [s[1] for s in similarities2],
        'Words': [f'{s1[0]}/{s2[0]}' for s1, s2 in zip(similarities1, similarities2)]
    })
    
    fig = px.bar(df, x='Words', y=[f'{lang1}', f'{lang2}'],
                 title='Semantic Field Comparison',
                 barmode='group',
                 color_discrete_sequence=['#FF4B4B', '#0068C9'])
    
    fig.update_layout(
        xaxis_title="Word Pairs",
        yaxis_title="Semantic Similarity",
        height=400
    )
    return fig

def main():
    st.set_page_config(page_title="Semantic Comparison", page_icon="🎯", layout="wide")
    
    st.title("🎯 Semantic Comparison Tool")
    st.markdown("""
    Explore how words and concepts relate across different languages! See the semantic relationships
    and understand cultural connections through AI-powered analysis.
    """)

    # Load model
    model = load_model()

    # Example selector
    st.sidebar.header("Quick Examples")
    if st.sidebar.button("Try an Example"):
        category = st.sidebar.selectbox("Choose category:", list(EXAMPLE_PAIRS.keys()))
        if category:
            st.session_state['example_pair'] = EXAMPLE_PAIRS[category]

    # Language and text input
    col1, col2 = st.columns(2)
    with col1:
        lang1 = st.selectbox("First Language", options=list(LANGUAGES.keys()), key='lang1')
        if 'example_pair' in st.session_state:
            default_text1 = st.session_state['example_pair'][lang1]
        else:
            default_text1 = ""
        text1 = st.text_area("Enter text", value=default_text1, height=100, key='text1')
        
    with col2:
        lang2 = st.selectbox("Second Language", options=list(LANGUAGES.keys()), key='lang2')
        if 'example_pair' in st.session_state:
            default_text2 = st.session_state['example_pair'][lang2]
        else:
            default_text2 = ""
        text2 = st.text_area("Enter text", value=default_text2, height=100, key='text2')

    # Analyze button
    if st.button("🔍 Analyze Semantic Relationship"):
        if text1 and text2:
            with st.spinner("Analyzing semantic relationships..."):
                # Get embeddings and calculate similarity
                embed1 = model.encode(text1)
                embed2 = model.encode(text2)
                similarity = compute_similarity(embed1, embed2)
                
                # Get semantic fields
                field1 = get_semantic_field(text1, LANGUAGES[lang1], model)
                field2 = get_semantic_field(text2, LANGUAGES[lang2], model)
                
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
                st.subheader("Semantic Field Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**{lang1} semantic field:**")
                    for word, sim in field1[:5]:
                        st.write(f"- {word}: {sim:.2f} {get_similarity_display(sim)}")
                with col2:
                    st.write(f"**{lang2} semantic field:**")
                    for word, sim in field2[:5]:
                        st.write(f"- {word}: {sim:.2f} {get_similarity_display(sim)}")

                # Visualization
                st.subheader("Comparative Analysis")
                fig = plot_semantic_comparison(field1, field2, lang1, lang2)
                st.plotly_chart(fig, use_container_width=True)

                # Interpretation
                with st.expander("📊 Interpretation Guide"):
                    st.markdown(f"""
                    **Similarity Score: {similarity:.2f}**
                    
                    This analysis shows:
                    1. **Direct Match:** {get_similarity_display(similarity)}
                    2. **Semantic Field Overlap:** How related concepts compare
                    3. **Cultural Context:** How the terms are used in each language
                    
                    {
                    "Strong match! These terms share very similar semantic spaces. They likely evoke similar concepts and uses in both languages." 
                    if similarity > 0.8 else 
                    "Good match! These terms are related but might have subtle differences in usage or connotation." 
                    if similarity > 0.6 else 
                    "Partial match. These terms share some meaning but might be used differently in each language." 
                    if similarity > 0.4 else 
                    "These terms show significant differences in meaning or usage between the languages."
                    }
                    """)

    # Help section
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        1. **Select languages** for comparison
        2. **Enter words or phrases** in both languages
        3. **Click Analyze** to see:
           - Similarity scores
           - Related concepts
           - Visual comparison
           
        **Tips:**
        - Try similar concepts across languages
        - Compare cultural terms
        - Look for patterns in semantic fields
        - Use example pairs to explore
        """)

if __name__ == "__main__":
    main()