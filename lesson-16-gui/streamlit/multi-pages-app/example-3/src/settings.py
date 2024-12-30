import streamlit as st

st.subheader("Settings")
st.write(f"You are logged in as {st.session_state.role}.")