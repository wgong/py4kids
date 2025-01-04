"""
Multi-Language Analysis Tool
--------------------------
A Streamlit app combining translation and semantic analysis capabilities.
"""

import streamlit as st
from utils.network_utils import check_internet

def main():
    st.set_page_config(
        page_title="Language Analysis Tools",
        page_icon="🌍",
        layout="wide"
    )

    st.title("🌍 Language Analysis Tools")
    st.markdown("""
    Welcome to our suite of language analysis tools! This application provides:
    
    1. 🔄 **Translation Tool**
       - Quick and easy translation between languages
       - Powered by Google Translate
       - Support for multiple languages
    
    2. 🎯 **Semantic Analysis**
       - Compare meanings across languages
       - Analyze semantic relationships
       - Understand cultural connections
    
    Choose a tool from the sidebar to get started!
    """)

    # Network status
    is_online = check_internet()
    status = "🌐 Online" if is_online else "📴 Offline"
    st.sidebar.write(f"Network Status: {status}")

    # Display feature availability
    st.subheader("📊 Feature Availability")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Translation Tool**")
        if is_online:
            st.success("✅ Available")
        else:
            st.error("❌ Requires Internet")
            
    with col2:
        st.write("**Semantic Analysis**")
        st.success("✅ Available (works offline)")

    # Tips section
    with st.expander("💡 Tips for Best Results"):
        st.markdown("""
        - Ensure internet connectivity for translations
        - Try both tools together for deeper understanding
        - Compare results across different language pairs
        - Use semantic analysis to verify translations
        - Experiment with cultural concepts
        """)

if __name__ == "__main__":
    main()