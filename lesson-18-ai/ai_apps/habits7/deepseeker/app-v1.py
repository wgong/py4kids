import sqlite3
import streamlit as st
import pandas as pd

# Database connection
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# Function to create the table
def create_table():
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks_7_habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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

# Function to add data
def add_data(task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, created_by, created_at, updated_by, updated_at):
    c.execute('''
    INSERT INTO tasks_7_habits (task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, created_by, created_at, updated_by, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, created_by, created_at, updated_by, updated_at))
    conn.commit()

# Function to view all data
def view_all_data():
    c.execute('SELECT * FROM tasks_7_habits')
    data = c.fetchall()
    return data

# Function to view all task names
def view_all_task_names():
    c.execute('SELECT DISTINCT task_name FROM tasks_7_habits')
    data = c.fetchall()
    return data

# Function to get task by name
def get_task(task_name):
    c.execute('SELECT * FROM tasks_7_habits WHERE task_name=?', (task_name,))
    data = c.fetchall()
    return data

# Function to get task by status
def get_task_by_status(status):
    c.execute('SELECT * FROM tasks_7_habits WHERE status=?', (status,))
    data = c.fetchall()
    return data

# Function to edit task data
def edit_task_data(new_task_name, new_description, new_task_group, new_is_urgent, new_is_important, new_status, new_pct_completed, new_category, new_note, new_updated_by, new_updated_at, task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, updated_by, updated_at):
    c.execute('''
    UPDATE tasks_7_habits SET task_name=?, description=?, task_group=?, is_urgent=?, is_important=?, status=?, pct_completed=?, category=?, note=?, updated_by=?, updated_at=?
    WHERE task_name=? AND description=? AND task_group=? AND is_urgent=? AND is_important=? AND status=? AND pct_completed=? AND category=? AND note=? AND updated_by=? AND updated_at=?
    ''', (new_task_name, new_description, new_task_group, new_is_urgent, new_is_important, new_status, new_pct_completed, new_category, new_note, new_updated_by, new_updated_at, task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, updated_by, updated_at))
    conn.commit()
    data = c.fetchall()
    return data

# Function to delete data
def delete_data(task_name):
    c.execute('DELETE FROM tasks_7_habits WHERE task_name=?', (task_name,))
    conn.commit()

# Streamlit app
def main():
    st.title("7 Habits Task Manager")

    menu = ["Home", "Add Task", "View Tasks", "Edit Task", "Delete Task", "7-Habits-View"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Welcome to the 7 Habits Task Manager. Use the sidebar to navigate through the app.")

    elif choice == "Add Task":
        st.subheader("Add a New Task")
        task_name = st.text_input("Task Name")
        description = st.text_area("Description")
        task_group = st.selectbox("Task Group", ["Work", "Personal", "Other"])
        is_urgent = st.selectbox("Is Urgent?", ["Y", "N"])
        is_important = st.selectbox("Is Important?", ["Y", "N"])
        status = st.selectbox("Status", ["", "ToDo", "Doing", "Done"])
        pct_completed = st.selectbox("Percentage Completed", ["0%", "25%", "50%", "75%", "100%"])
        category = st.selectbox("Category", ["", "learning", "research", "project", "fun"])
        note = st.text_area("Note")
        created_by = st.text_input("Created By")
        created_at = st.text_input("Created At")
        updated_by = st.text_input("Updated By")
        updated_at = st.text_input("Updated At")

        if st.button("Add Task"):
            add_data(task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, created_by, created_at, updated_by, updated_at)
            st.success("Task Added: {}".format(task_name))

    elif choice == "View Tasks":
        st.subheader("View All Tasks")
        result = view_all_data()
        df = pd.DataFrame(result, columns=["ID", "Task Name", "Description", "Task Group", "Is Urgent", "Is Important", "Status", "Percentage Completed", "Category", "Note", "Created By", "Created At", "Updated By", "Updated At"])
        st.dataframe(df)

    elif choice == "Edit Task":
        st.subheader("Edit Task")
        task_name = st.selectbox("Select Task", [task[0] for task in view_all_task_names()])
        task_data = get_task(task_name)
        if task_data:
            task_name = task_data[0][1]
            description = task_data[0][2]
            task_group = task_data[0][3]
            is_urgent = task_data[0][4]
            is_important = task_data[0][5]
            status = task_data[0][6]
            pct_completed = task_data[0][7]
            category = task_data[0][8]
            note = task_data[0][9]
            created_by = task_data[0][10]
            created_at = task_data[0][11]
            updated_by = task_data[0][12]
            updated_at = task_data[0][13]

            new_task_name = st.text_input("Task Name", task_name)
            new_description = st.text_area("Description", description)
            new_task_group = st.selectbox("Task Group", ["Work", "Personal", "Other"], index=["Work", "Personal", "Other"].index(task_group))
            new_is_urgent = st.selectbox("Is Urgent?", ["Y", "N"], index=["Y", "N"].index(is_urgent))
            new_is_important = st.selectbox("Is Important?", ["Y", "N"], index=["Y", "N"].index(is_important))
            new_status = st.selectbox("Status", ["", "ToDo", "Doing", "Done"], index=["", "ToDo", "Doing", "Done"].index(status))
            new_pct_completed = st.selectbox("Percentage Completed", ["0%", "25%", "50%", "75%", "100%"], index=["0%", "25%", "50%", "75%", "100%"].index(pct_completed))
            new_category = st.selectbox("Category", ["", "learning", "research", "project", "fun"], index=["", "learning", "research", "project", "fun"].index(category))
            new_note = st.text_area("Note", note)
            new_updated_by = st.text_input("Updated By", updated_by)
            new_updated_at = st.text_input("Updated At", updated_at)

            if st.button("Update Task"):
                edit_task_data(new_task_name, new_description, new_task_group, new_is_urgent, new_is_important, new_status, new_pct_completed, new_category, new_note, new_updated_by, new_updated_at, task_name, description, task_group, is_urgent, is_important, status, pct_completed, category, note, updated_by, updated_at)
                st.success("Task Updated: {}".format(new_task_name))

    elif choice == "Delete Task":
        st.subheader("Delete Task")
        task_name = st.selectbox("Select Task", [task[0] for task in view_all_task_names()])
        if st.button("Delete Task"):
            delete_data(task_name)
            st.success("Task Deleted: {}".format(task_name))

    elif choice == "7-Habits-View":
        st.subheader("7 Habits View")

        # Filters
        task_groups = ["Work", "Personal", "Other"]
        statuses = ["", "ToDo", "Doing", "Done"]
        selected_task_groups = st.multiselect("Filter by Task Group", task_groups, default=task_groups)
        selected_statuses = st.multiselect("Filter by Status", statuses, default=statuses)

        # Fetch all tasks
        all_tasks = view_all_data()
        df = pd.DataFrame(all_tasks, columns=["ID", "Task Name", "Description", "Task Group", "Is Urgent", "Is Important", "Status", "Percentage Completed", "Category", "Note", "Created By", "Created At", "Updated By", "Updated At"])

        # Apply filters
        filtered_df = df[(df['Task Group'].isin(selected_task_groups)) & (df['Status'].isin(selected_statuses))]

        # Divide tasks into quadrants
        quadrant_I = filtered_df[(filtered_df['Is Important'] == 'Y') & (filtered_df['Is Urgent'] == 'Y')]
        quadrant_II = filtered_df[(filtered_df['Is Important'] == 'N') & (filtered_df['Is Urgent'] == 'Y')]
        quadrant_III = filtered_df[(filtered_df['Is Important'] == 'N') & (filtered_df['Is Urgent'] == 'N')]
        quadrant_IV = filtered_df[(filtered_df['Is Important'] == 'Y') & (filtered_df['Is Urgent'] == 'N')]

        # Display quadrants
        st.write("### Quadrant I: Important/Urgent")
        st.dataframe(quadrant_I)

        st.write("### Quadrant II: Un-Important/Urgent")
        st.dataframe(quadrant_II)

        st.write("### Quadrant III: Un-Important/Un-Urgent")
        st.dataframe(quadrant_III)

        st.write("### Quadrant IV: Important/Un-Urgent")
        st.dataframe(quadrant_IV)

if __name__ == '__main__':
    create_table()
    main()