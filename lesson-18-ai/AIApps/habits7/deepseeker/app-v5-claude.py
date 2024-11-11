import streamlit as st
import sqlite3
import hashlib
from datetime import datetime, date
import pandas as pd
from st_aggrid import (
    AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
)

# ... (keep all the existing constants and imports)

# Function to check if the user is the first user (super-user)
def is_first_user():
    c.execute(f"SELECT COUNT(*) FROM {TABLE_H7_USER}")
    count = c.fetchone()[0]
    return count == 0

# Modified add_user function
def add_user(email, password, username, is_admin=0, is_active=1, profile="", note=""):
    hashed_password = hash_password(password)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if is_first_user():
        is_admin = 1
    c.execute(f'''
    INSERT INTO {TABLE_H7_USER} (email, password, username, is_admin, is_active, profile, note, created_by, created_at, updated_by, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (email, hashed_password, username, is_admin, is_active, profile, note, email, now, email, now))
    conn.commit()

# Function to get all users
def get_all_users():
    c.execute(f"SELECT id, email, username, is_admin, is_active FROM {TABLE_H7_USER}")
    return c.fetchall()

# Function to update user
def update_user(user_id, email, username, is_admin, is_active, profile, note):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(f'''
    UPDATE {TABLE_H7_USER}
    SET email=?, username=?, is_admin=?, is_active=?, profile=?, note=?, updated_at=?
    WHERE id=?
    ''', (email, username, is_admin, is_active, profile, note, now, user_id))
    conn.commit()

# Modified verify_user function
def verify_user(email, password):
    hashed_password = hash_password(password)
    c.execute(f"SELECT * FROM {TABLE_H7_USER} WHERE email = ? AND password = ? AND is_active = 1", (email, hashed_password))
    user = c.fetchone()
    return user

# Function to get user by id
def get_user_by_id(user_id):
    c.execute(f"SELECT * FROM {TABLE_H7_USER} WHERE id = ?", (user_id,))
    return c.fetchone()

# New function for the Edit User page
def edit_user_page(user_id, is_admin):
    st.subheader("Edit User")
    user = get_user_by_id(user_id)
    if user:
        email = st.text_input("Email", value=user[1])
        username = st.text_input("Username", value=user[3])
        profile = st.text_area("Profile", value=user[6] or "")
        note = st.text_area("Note", value=user[7] or "")
        
        if is_admin:
            is_admin_flag = st.checkbox("Is Admin", value=bool(user[4]))
            is_active = st.checkbox("Is Active", value=bool(user[5]))
        else:
            is_admin_flag = user[4]
            is_active = user[5]

        if st.button("Update User"):
            update_user(user_id, email, username, int(is_admin_flag), int(is_active), profile, note)
            st.success("User updated successfully")
            st.rerun()

# New function for the Add User page (admin only)
def add_user_page():
    st.subheader("Add User")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    is_admin = st.checkbox("Is Admin")
    is_active = st.checkbox("Is Active", value=True)
    profile = st.text_area("Profile")
    note = st.text_area("Note")

    if st.button("Add User"):
        if password != confirm_password:
            st.error("Passwords do not match")
        elif email_exists(email):
            st.error("Email already exists")
        else:
            add_user(email, password, username, int(is_admin), int(is_active), profile, note)
            st.success("User added successfully")

# New function for the Manage Users page (admin only)
def manage_users_page():
    st.subheader("Manage Users")
    users = get_all_users()
    df = pd.DataFrame(users, columns=["ID", "Email", "Username", "Is Admin", "Is Active"])
    grid_resp = _display_df_grid(df, key_name="users_grid")

    if grid_resp['selected_rows']:
        selected_user = grid_resp['selected_rows'][0]
        st.subheader(f"Edit User: {selected_user['Username']}")
        email = st.text_input("Email", value=selected_user['Email'])
        username = st.text_input("Username", value=selected_user['Username'])
        is_admin = st.checkbox("Is Admin", value=bool(selected_user['Is Admin']))
        is_active = st.checkbox("Is Active", value=bool(selected_user['Is Active']))
        user = get_user_by_id(selected_user['ID'])
        profile = st.text_area("Profile", value=user[6] or "")
        note = st.text_area("Note", value=user[7] or "")

        if st.button("Update User"):
            update_user(selected_user['ID'], email, username, int(is_admin), int(is_active), profile, note)
            st.success("User updated successfully")
            st.rerun()

# Modified login page
def login_page():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = verify_user(email, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = user[0]
            st.session_state['username'] = user[3]
            st.session_state['is_admin'] = bool(user[4])
            st.success(f"Logged in as {user[3]}")
            st.rerun()
        else:
            st.error("Incorrect email or password or account is inactive")

# Modified registration page
def registration_page():
    st.subheader("Register")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match")
        elif email_exists(email):
            st.error("Email already exists")
        else:
            add_user(email, password, username)
            st.success("Registration successful. Please login.")

# Modified main function
def main():
    st.sidebar.subheader("7 Habits Task Manager")

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Sidebar for login/logout
    if st.session_state['logged_in']:
        st.sidebar.write(f"Logged in as: {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['user_id'] = None
            st.session_state['username'] = None
            st.session_state['is_admin'] = False
            st.rerun()
    else:
        auth_option = st.sidebar.radio("Choose an option", ["Login", "Register"])
        if auth_option == "Login":
            login_page()
        else:
            registration_page()

    # Only show the main app if logged in
    if not st.session_state['logged_in']:
        return
    
    user_id = st.session_state['user_id']
    is_admin = st.session_state['is_admin']
    
    menu = ["Home", "7-Habits-Task View", "View Tasks", "Add Task", "Edit Task", "Delete Task", "Edit User"]
    if is_admin:
        menu.extend(["Add User", "Manage Users"])

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        # ... (keep existing Home code)

    elif choice == "Add Task":
        # ... (keep existing Add Task code)

    elif choice == "View Tasks":
        # ... (keep existing View Tasks code)

    elif choice == "Edit Task":
        # ... (keep existing Edit Task code)

    elif choice == "Delete Task":
        # ... (keep existing Delete Task code)

    elif choice == "7-Habits-Task View":
        # ... (keep existing 7-Habits-Task View code)

    elif choice == "Edit User":
        edit_user_page(user_id, is_admin)

    elif choice == "Add User" and is_admin:
        add_user_page()

    elif choice == "Manage Users" and is_admin:
        manage_users_page()


if __name__ == '__main__':
    create_task_table()
    create_user_table()
    main()