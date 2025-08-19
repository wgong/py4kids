import streamlit as st
import time

if "counter" not in st.session_state:
    st.session_state.counter = 0

def increment_counter():
    st.session_state.counter += 1
    st.write(f"Counter: {st.session_state.counter}")

def dynamic_slider():
    st.header("Dynamic Slider")
    value = st.slider("Adjust value", 0, 100, 25)
    st.write(f"Selected: {value}")
    st.write(f"Last updated: {time.strftime('%H:%M:%S')}")

@st.fragment
def dynamic_slider_fragment():
    st.header("Dynamic Slider")
    value = st.slider("Adjust value", 0, 100, 25)
    st.write(f"Selected: {value}")
    st.write(f"Last updated: {time.strftime('%H:%M:%S')}")

def main():
    enable_fragment = st.checkbox("Enable Fragment", value=True)
    if enable_fragment:
        dynamic_slider_fragment()
    else:
        dynamic_slider()
    
    st.header("Dynamic Slider with Static Text")
    st.write("This static text doesn't reload when slider changes")
    increment_counter()

if __name__ == "__main__":
    st.title("Fragment Demo")
    main()