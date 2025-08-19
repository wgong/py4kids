import streamlit as st

@st.fragment
def parent_fragment():
    st.header("Parent Fragment")
    parent_value = st.slider("Parent value", 0, 10, 5)
    
    @st.fragment
    def child_fragment():
        st.subheader("Child Fragment")
        child_value = st.slider("Child value", 0, 10, 5)
        st.write(f"Parent: {parent_value}, Child: {child_value}")
    
    _, c2 = st.columns([1,4])
    with c2:
        child_fragment()
        

def main():
    st.title("Nested Fragments")
    parent_fragment()
    st.write("Main app content")

if __name__ == "__main__":
    main()