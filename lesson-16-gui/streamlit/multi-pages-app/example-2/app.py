"""
https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
"""


import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.write("you are at log in page")
    if st.sidebar.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    st.write("you are at log out page")
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

# pages are defined by functions
login_page = st.Page(
    login, title="Log in", icon=":material/login:"
)
logout_page = st.Page(
    logout, title="Log out", icon=":material/logout:"
)

# pages are defined by files
dashboard = st.Page(
    "reports/dashboard.py", title="Dashboard", icon=":material/dashboard:"
)
bugs = st.Page(
    "reports/bugs.py", title="Bug reports", icon=":material/bug_report:", default=True
)
alerts = st.Page(
    "reports/alerts.py", title="System alerts", icon=":material/notification_important:"
)

search = st.Page(
    "tools/search.py", title="Search", icon=":material/search:"
)
history = st.Page(
    "tools/history.py", title="History", icon=":material/history:"
)

# define navigations
if st.session_state.logged_in:
    pg = st.navigation({
            "Account": [logout_page],
            "Reports": [dashboard, bugs, alerts],
            "Tools": [search, history],
        })
else:
    pg = st.navigation([login_page])

pg.run()