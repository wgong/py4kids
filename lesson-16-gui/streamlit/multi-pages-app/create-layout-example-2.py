import os

def create_project_structure():
    # Define the base directory
    base_dir = "example-2"
    
    # Create the base directory
    os.makedirs(base_dir, exist_ok=True)
    
    # Create reports directory and its files
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # Create files in reports directory
    report_files = ["alerts.py", "bugs.py", "dashboard.py"]
    for file in report_files:
        with open(os.path.join(reports_dir, file), 'w') as f:
            pass
    
    # Create tools directory and its files
    tools_dir = os.path.join(base_dir, "tools")
    os.makedirs(tools_dir, exist_ok=True)
    
    # Create files in tools directory
    tool_files = ["history.py", "search.py"]
    for file in tool_files:
        with open(os.path.join(tools_dir, file), 'w') as f:
            pass
    
    # Create streamlit app file
    with open(os.path.join(base_dir, "app.py"), 'w') as f:
        pass

    print("Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()