import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Set page configuration to wide layout
st.set_page_config(layout="wide")

# Database connection
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# Create table
def create_table():
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks_7_habits(
        id INTEGER PRIMARY KEY,
        task_name TEXT NOT NULL,
        description TEXT,
        task_group TEXT DEFAULT 'Personal' CHECK(task_group IN ('Work', 'Personal', 'Other')),
        is_urgent TEXT DEFAULT 'N' CHECK(is_urgent IN ('Y', 'N')),
        is_important TEXT DEFAULT 'N' CHECK(is_important IN ('Y', 'N')),
        status TEXT DEFAULT '' CHECK(status IN ('', 'ToDo', 'Doing', 'Done')),
        pct_completed TEXT DEFAULT '0%' CHECK(pct_completed IN ('0%', '25%', '50%', '75%', '100%')),
        category TEXT DEFAULT '' CHECK(category IN ('', 'learning', 'research', 'project', 'fun')),
        note TEXT,
        created_by TEXT,
        created_at TEXT,
        updated_by TEXT,
        updated_at TEXT
    )
    ''')
    conn.commit()

# Add data
def add_data(task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, created_by):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
    INSERT INTO tasks_7_habits(task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, created_by, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, created_by, created_at))
    conn.commit()

# View all data
def view_all_data():
    c.execute('SELECT * FROM tasks_7_habits')
    data = c.fetchall()
    return data

# Get tasks by importance and urgency
def get_tasks_by_importance_urgency(is_important, is_urgent, task_groups, statuses):
    query = '''
    SELECT * FROM tasks_7_habits 
    WHERE is_important=? AND is_urgent=? 
    AND task_group IN ({})
    AND status IN ({})
    '''.format(','.join(['?']*len(task_groups)), ','.join(['?']*len(statuses)))
    c.execute(query, (is_important, is_urgent) + tuple(task_groups) + tuple(statuses))
    data = c.fetchall()
    return data

# Get task by id
def get_task_by_id(task_id):
    c.execute('SELECT * FROM tasks_7_habits WHERE id=?', (task_id,))
    data = c.fetchone()
    return data

# Update task
def update_task(task_id, task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, updated_by):
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
    UPDATE tasks_7_habits
    SET task_name=?, description=?, task_group=?, is_urgent=?, is_important=?, status=?, pct_completed=?, category=?, note=?, updated_by=?, updated_at=?
    WHERE id=?
    ''', (task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, updated_by, updated_at, task_id))
    conn.commit()

# Streamlit app
def main():
    st.title("7 Habits Todo App")
    
    create_table()
    
    menu = ["Home", "View Tasks", "Add Task", "Edit Task", "7-Habits-View"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.subheader("Welcome to the 7 Habits Todo App!")
        st.write("""
        This app is based on the principles from the book "The 7 Habits of Highly Effective People" by Stephen Covey.
        It helps you organize your tasks based on their importance and urgency.
        """)
        st.markdown("""
        - Learn more about [Stephen Covey](https://en.wikipedia.org/wiki/Stephen_Covey) on Wikipedia.
        - This app is powered by [Streamlit](https://docs.streamlit.io/). Check out their documentation for more information.
        """)
        
    elif choice == "View Tasks":
        st.subheader("View Tasks")
        result = view_all_data()
        df = pd.DataFrame(result, columns=['id', 'task_name', 'description', 'task_group', 'is_urgent', 'is_important', 'status', 'pct_completed', 'category', 'note', 'created_by', 'created_at', 'updated_by', 'updated_at'])
        st.dataframe(df)
        
    elif choice == "Add Task":
        st.subheader("Add Task")
        col1, col2 = st.columns(2)
        
        with col1:
            task_name = st.text_input("Task Name")
            description = st.text_area("Description")
            task_group = st.selectbox("Task Group", ["Personal", "Work", "Other"])
            is_urgent = st.selectbox("Is Urgent?", ["N", "Y"])
            is_important = st.selectbox("Is Important?", ["N", "Y"])
        
        with col2:
            status = st.selectbox("Status", ["", "ToDo", "Doing", "Done"])
            pct_completed = st.selectbox("Percentage Completed", ["0%", "25%", "50%", "75%", "100%"])
            category = st.selectbox("Category", ["", "learning", "research", "project", "fun"])
            note = st.text_area("Note")
            created_by = st.text_input("Created By")
        
        if st.button("Add Task"):
            add_data(task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, created_by)
            st.success("Task '{}' added successfully!".format(task_name))

    elif choice == "Edit Task":
        st.subheader("Edit Task")
        
        # Get all tasks
        tasks = view_all_data()
        
        # Create a list of task options
        task_options = [f"{task[1]} ({task[6]}) [{task[3]}]" for task in tasks]
        task_dict = {f"{task[1]} ({task[6]}) [{task[3]}]": task[0] for task in tasks}
        
        # Select task to edit
        selected_task = st.selectbox("Select a task to edit", task_options)
        
        if selected_task:
            task_id = task_dict[selected_task]
            task = get_task_by_id(task_id)
            
            col1, col2 = st.columns(2)
            
            with col1:
                task_name = st.text_input("Task Name", value=task[1])
                description = st.text_area("Description", value=task[2])
                task_group = st.selectbox("Task Group", ["Personal", "Work", "Other"], index=["Personal", "Work", "Other"].index(task[3]))
                is_urgent = st.selectbox("Is Urgent?", ["N", "Y"], index=["N", "Y"].index(task[4]))
                is_important = st.selectbox("Is Important?", ["N", "Y"], index=["N", "Y"].index(task[5]))
            
            with col2:
                status = st.selectbox("Status", ["", "ToDo", "Doing", "Done"], index=["", "ToDo", "Doing", "Done"].index(task[6]))
                pct_completed = st.selectbox("Percentage Completed", ["0%", "25%", "50%", "75%", "100%"], index=["0%", "25%", "50%", "75%", "100%"].index(task[7]))
                category = st.selectbox("Category", ["", "learning", "research", "project", "fun"], index=["", "learning", "research", "project", "fun"].index(task[8]))
                note = st.text_area("Note", value=task[9])
                updated_by = st.text_input("Updated By")
            
            if st.button("Update Task"):
                update_task(task_id, task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, updated_by)
                st.success("Task '{}' updated successfully!".format(task_name))
            
    elif choice == "7-Habits-View":
        st.subheader("7 Habits View")
        
        # Global filters
        col1, col2 = st.columns(2)
        with col1:
            task_groups = st.multiselect("Select Task Groups", ["Personal", "Work", "Other"], default=["Personal", "Work", "Other"])
        with col2:
            statuses = st.multiselect("Select Statuses", ["", "ToDo", "Doing", "Done"], default=["", "ToDo", "Doing", "Done"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("II. Urgent / Not Important")
            df_q2 = pd.DataFrame(get_tasks_by_importance_urgency('N', 'Y', task_groups, statuses), 
                                 columns=['id', 'task_name', 'description', 'task_group', 'is_urgent', 'is_important', 'status', 'pct_completed', 'category', 'note', 'created_by', 'created_at', 'updated_by', 'updated_at'])
            st.dataframe(df_q2)
            
            st.subheader("III. Not Urgent / Not Important")
            df_q3 = pd.DataFrame(get_tasks_by_importance_urgency('N', 'N', task_groups, statuses), 
                                 columns=['id', 'task_name', 'description', 'task_group', 'is_urgent', 'is_important', 'status', 'pct_completed', 'category', 'note', 'created_by', 'created_at', 'updated_by', 'updated_at'])
            st.dataframe(df_q3)
        
        with col2:
            st.subheader("I. Urgent / Important")
            df_q1 = pd.DataFrame(get_tasks_by_importance_urgency('Y', 'Y', task_groups, statuses), 
                                 columns=['id', 'task_name', 'description', 'task_group', 'is_urgent', 'is_important', 'status', 'pct_completed', 'category', 'note', 'created_by', 'created_at', 'updated_by', 'updated_at'])
            st.dataframe(df_q1)
            
            st.subheader("IV. Not Urgent / Important")
            df_q4 = pd.DataFrame(get_tasks_by_importance_urgency('Y', 'N', task_groups, statuses), 
                                 columns=['id', 'task_name', 'description', 'task_group', 'is_urgent', 'is_important', 'status', 'pct_completed', 'category', 'note', 'created_by', 'created_at', 'updated_by', 'updated_at'])
            st.dataframe(df_q4)

if __name__ == '__main__':
    main()