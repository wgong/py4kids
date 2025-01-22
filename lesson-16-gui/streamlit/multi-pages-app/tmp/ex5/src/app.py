import streamlit as st

st.title("Streamlit Multipage Demo")

# Logo
try:
    st.image(
        "docs/st_app_logo.png",
        caption="App Logo"
    )
except Exception:
    st.write("Logo not found")

# Role management
NO_ROLE = ""
if "role" not in st.session_state:
    st.session_state.role = NO_ROLE

role_list = [NO_ROLE, "Requester", "Responder", "Admin"]

def login():
    st.markdown("""
### What is Streamlit Multipage App ?
- [Concept of Multipage Apps](https://docs.streamlit.io/develop/concepts/multipage-apps)
- [Create dynamic navigation menus](https://docs.streamlit.io/develop/tutorials/multipage/dynamic-navigation)
""")
    st.sidebar.subheader("Log in")
    role = st.sidebar.selectbox("Choose a role", role_list)
    if st.sidebar.button("Log in"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = NO_ROLE
    st.rerun()

role = st.session_state.role

# Base pages
login_page = st.Page(
    login,
)

logout_page = st.Page(
    logout,
    title="Log out",
    icon=":material/logout:"
)

settings_page = st.Page(
    "settings.py",
    title="Settings",
    icon=":material/settings:"
)



# Page grouping
account_pages = [logout_page, settings_page]

# Dynamic navigation based on role
page_dict = {}
if role:
    if role in ["Requester", "Admin"]:
        page_dict["Request"] = request_pages
    if role in ["Responder", "Admin"]:
        page_dict["Respond"] = respond_pages
    if role in ["Admin"]:
        page_dict["Admin"] = admin_pages

# Final page layout
page_layout = ({"Account": account_pages} | page_dict) if len(page_dict) > 0 else [login_page]
pg = st.navigation(page_layout)
pg.run()
