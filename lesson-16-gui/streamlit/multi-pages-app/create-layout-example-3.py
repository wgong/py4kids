import os

def create_app_file(dir_name, file_name):
    content = f"""import streamlit as st

st.title(f"{dir_name}/{file_name}")
"""
    with open(os.path.join(dir_name, file_name), 'w') as f:
        f.write(content)

def create_page_file(dir_name, file_name):
    content = f"""import streamlit as st

st.title(f"{dir_name}/{file_name}")
"""

    # overwrite    
    if file_name == "admin_1.py":
        content = """
import streamlit as st

st.header("Admin 1")
st.write(f"You are logged in as {st.session_state.role}.")
"""

    with open(os.path.join(dir_name, file_name), 'w') as f:
        f.write(content)


def create_project_structure():
    # Create the base directory
    base_dir = "example-3"
    os.makedirs(base_dir, exist_ok=True)
    
    admin_dir = os.path.join(base_dir, "admin")
    os.makedirs(admin_dir, exist_ok=True)  
    # Create files in this directory
    report_files = ["admin_1.py", "admin_2.py",]
    for file in report_files:
        create_page_file(dir_name=admin_dir, file_name=file)
    
    request_dir = os.path.join(base_dir, "request")
    os.makedirs(request_dir, exist_ok=True)  
    # Create files in tools directory
    tool_files = ["request_1.py", "request_2.py"]
    for file in tool_files:
        create_page_file(dir_name=request_dir, file_name=file)

    respond_dir = os.path.join(base_dir, "respond")
    os.makedirs(respond_dir, exist_ok=True)
    # Create files in tools directory
    tool_files = ["respond_1.py", "respond_2.py"]
    for file in tool_files:
        create_page_file(dir_name=respond_dir, file_name=file)

    # Create streamlit app file
    create_page_file(dir_name=base_dir, file_name="app.py")

    print("Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()