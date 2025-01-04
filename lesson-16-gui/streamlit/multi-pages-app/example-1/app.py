import streamlit as st

st.set_page_config(page_title="Multi-Page-App", page_icon=":material/edit:")

page_1 = st.Page("page_1.py", title="Create entry", icon=":material/add_circle:")
page_2 = st.Page("page_2.py", title="Delete entry", icon=":material/delete:")

pg = st.navigation([page_1, page_2])
pg.run()