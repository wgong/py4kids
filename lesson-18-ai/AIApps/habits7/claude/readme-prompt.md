## Requirements

Adopting the approach recommended in the book `7 Habits of Highly Effective People` by Stephen Covey, I design a table called `tasks_7_habits` to store tasks which has the following columns:
"""
id  (int) : primary key (required)
task_name (text) : short task name  (required)
description (text) : long description
task_group (text) : bound list of ("Work", "Personal", "Other") with "Personal" as default
is_urgent (text) : bound list of ("Y", "N") for Yes/No with "N" as default
is_important (text) : bound list of ("Y", "N") for Yes/No with "N" as default
status (text) : bound list of ("", "ToDo", "Doing", "Done") with "" as default
pct_completed (text) : bound list of ("0%", "25%", "50%", "75%", "100%") with "0%" as default
category (text) : bound list of ("", "learning", "research", "project", "fun") with "" as default
note (text) : comment
created_by (text) : user_id (optional)
created_at (text) : timestamp string
updated_by (text) : user_id (optional)
updated_at (text) : timestamp string
"""

Can you refactor this simple streamlit app with python code: """ 

import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT,task_status TEXT,task_due_date DATE)')


def add_data(task,task_status,task_due_date):
	c.execute('INSERT INTO taskstable(task,task_status,task_due_date) VALUES (?,?,?)',(task,task_status,task_due_date))
	conn.commit()


def view_all_data():
	c.execute('SELECT * FROM taskstable')
	data = c.fetchall()
	return data

def view_all_task_names():
	c.execute('SELECT DISTINCT task FROM taskstable')
	data = c.fetchall()
	return data

def get_task(task):
	c.execute('SELECT * FROM taskstable WHERE task="{}"'.format(task))
	data = c.fetchall()
	return data

def get_task_by_status(task_status):
	c.execute('SELECT * FROM taskstable WHERE task_status="{}"'.format(task_status))
	data = c.fetchall()


def edit_task_data(new_task,new_task_status,new_task_date,task,task_status,task_due_date):
	c.execute("UPDATE taskstable SET task =?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=? ",(new_task,new_task_status,new_task_date,task,task_status,task_due_date))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(task):
	c.execute('DELETE FROM taskstable WHERE task="{}"'.format(task))
	conn.commit()
"""

by adding a new menu item called "7-Habits-View", when selected, it will display all tasks into a page divided into 4 quadrants : 
(I) Important/Urgent (is_important=Y and is_urgent=Y) - displayed at upper right;
(II) Un-Important/Urgent (is_important=N and is_urgent=Y) - displayed at upper left;
(III) Un-Important/Un-Urgent (is_important=N and is_urgent=N) - displayed at lower left;
(IV) Important/Un-Urgent (is_important=Y and is_urgent=N) - displayed at lower right;

For the time being, display list of tasks within each quadrant by using `st.dataframe()` API.

There should be 2 global filters (placed at the top of page):
1) by `task_group` attribute as `st.multiselect` selection
2) by `status` attribute as `st.multiselect` selection

=> app-v2.py

You are a hero, everything works like a charm. Don't you forget a menu item to "Edit Task", please add that? For the time being, you can simply list all the tasks in st.selectbox​ with its display value as formatted by concatinating "task_name (status) [task_group]"

=> app-v3.py

Your revision also looks good. I feel my prompt is effective in boot-strapping this streamlit app so quickly with your mighty help (I actually have a few years of streamlit dev experiences ) , what do you think? I am satisfied with today's work, I will review your generated code more carefully before going for more enhancements.  I could think of the following features 1) replace task list with ag-grid streamlit component with pagination and single select; 2) merge add/update/delete (CRUD) into a single form; 3) add a dashboard to track task progress. What do you think of my plan?

Those 4 suggestions are excellent, I do plan to release this app to streamlit community as a give-back and deploy it to streamlit cloud to support multi-users. An integration feature with import and export capabilities would also be desirable

=> app-v4.py


## Claude

[Tasks-7-Habits](https://claude.ai/chat/ce85afde-bcb8-4923-a6f4-1e8e3bf56f0c)

## Source
- https://github.com/wgong/tasks-7-habits