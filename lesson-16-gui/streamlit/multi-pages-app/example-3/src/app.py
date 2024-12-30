"""
https://docs.streamlit.io/develop/tutorials/multipage/dynamic-navigation
"""

import streamlit as st

st.title("Streamlit Multi-page Demo")
st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

NO_ROLE = ""
if "role" not in st.session_state:
    st.session_state.role = NO_ROLE

role_list = [NO_ROLE, "Requester", "Responder", "Admin"]

def login():
    st.header("Log in")
    role = st.selectbox("Choose your role", role_list)
    if st.button("Log in"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = NO_ROLE
    st.rerun()

role = st.session_state.role

login_page = st.Page(login)

logout_page = st.Page(
    logout, 
    title="Log out", 
    icon=":material/logout:"
)

settings = st.Page(
    "settings.py", 
    title="Settings", 
    icon=":material/settings:"
)

request_1 = st.Page(
    "request/request_1.py",
    title="Request 1",
    icon=":material/help:",
    default=(role == "Requester"),
)
request_2 = st.Page(
    "request/request_2.py", 
    title="Request 2", 
    icon=":material/bug_report:"
)
respond_1 = st.Page(
    "respond/respond_1.py",
    title="Respond 1",
    icon=":material/healing:",
    default=(role == "Responder"),
)
respond_2 = st.Page(
    "respond/respond_2.py", 
    title="Respond 2", 
    icon=":material/handyman:"
)
admin_1 = st.Page(
    "admin/admin_1.py",
    title="Admin 1",
    icon=":material/person_add:",
)
admin_2 = st.Page(
    "admin/admin_2.py", 
    title="Admin 2", 
    icon=":material/security:",
    default=(role == "Admin"),
)

# grouping pages
account_pages = [logout_page, settings]
request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2]

page_dict = {}
if role:
    if role in ["Requester", "Admin"]:
        page_dict["Request"] = request_pages
    if role in ["Responder", "Admin"]:
        page_dict["Respond"] = respond_pages
    if role in ["Admin"]:
        page_dict["Admin"] = admin_pages

page_layout = ({"Account": account_pages} | page_dict) if len(page_dict) > 0 else [login_page]
pg = st.navigation(page_layout)
pg.run()