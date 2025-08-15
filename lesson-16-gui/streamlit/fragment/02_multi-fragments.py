import streamlit as st
import time

@st.fragment
def temperature_converter():
    st.subheader("temperature_converter")
    celsius = st.slider("Celsius", -100, 100, 0)
    fahrenheit = (celsius * 9/5) + 32
    st.write(f"{celsius}°C = {fahrenheit:.1f}°F")
    st.caption(f"Updated at {time.strftime('%H:%M:%S')}")

@st.fragment
def color_picker():
    st.subheader("color_picker")
    color = st.color_picker("Choose a color", "#00f900")
    st.markdown(f"### Selected color: {color}")
    st.markdown(f'<div style="width:100px; height:100px; background-color:{color}"></div>', unsafe_allow_html=True)

def main():
    c1, _, c2 = st.columns([3,1,3])
    with c1:
        temperature_converter()
    with c2:
        color_picker()

if __name__ == "__main__":
    st.header("Independent Widgets")
    main()