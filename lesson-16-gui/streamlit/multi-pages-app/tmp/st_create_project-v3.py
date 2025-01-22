import os
import yaml
import click
from pathlib import Path
from typing import Optional, Union, List, Dict

def get_default_output_dir(yaml_file: str) -> str:
    """Extract default output directory name from YAML filename."""
    return Path(yaml_file).stem

def extract_pages_from_structure(structure: dict) -> dict:
    """
    Extract pages from the YAML structure.
    Returns a dictionary of section names and their Python files.
    """
    pages = {}
    root_name = list(structure.keys())[0]
    root_content = structure[root_name]

    def process_items(items, current_path=""):
        for item in items:
            if isinstance(item, dict):
                for name, content in item.items():
                    if name == "src":
                        # Process src directory specially
                        if isinstance(content, dict):
                            for section, section_content in content.items():
                                if section in ["admin", "request", "respond"]:
                                    if isinstance(section_content, list):
                                        pages[section] = [f for f in section_content if f.endswith('.py')]
                    else:
                        # Process other directories
                        if isinstance(content, list):
                            py_files = [f for f in content if f.endswith('.py')]
                            if py_files:
                                pages[name] = py_files

    process_items(root_content)
    return pages

def generate_app_content(structure: dict) -> str:
    """Generate the app.py content based on the project structure."""
    pages = extract_pages_from_structure(structure)
    
    # Start with the base imports and setup
    content = '''import streamlit as st

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

'''
    
    # Add page definitions for each section
    for section, files in pages.items():
        if section not in ['admin', 'request', 'respond']:
            continue

        # Add section pages
        for file in sorted(files):  # Sort to ensure consistent order
            page_name = file.replace('.py', '')
            title = page_name.replace('_', ' ').title()
            
            # Choose icon based on section
            if section == 'admin':
                icon = ":material/security:"
            elif section == 'request':
                icon = ":material/help:"
            elif section == 'respond':
                icon = ":material/healing:"
            
            content += f'''
{page_name}_page = st.Page(
    "{section}/{file}",
    title="{title}",
    icon="{icon}",
    default=(role == "{section.title()}")
)'''

    # Add page grouping and navigation
    content += '''

# Page grouping
account_pages = [logout_page, settings_page]'''

    # Add section page groups
    for section in ['request', 'respond', 'admin']:
        if section in pages:
            page_names = [f"{f.replace('.py', '')}_page" for f in sorted(pages[section])]
            content += f'''
{section}_pages = [{', '.join(page_names)}]'''

    # Add navigation logic
    content += '''

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
'''
    return content

def create_file_content(file_path: str, dir_name: str, file_name: str, complete_structure: dict = None) -> str:
    """Generate content for files based on their type and location."""
    if not file_name.endswith('.py'):
        if file_name.endswith('requirements.txt'):
            return "streamlit>=1.32.0"
        return ''  # Empty content for non-Python files
        
    if file_name == "app.py" and complete_structure:
        return generate_app_content(complete_structure)
        
    if file_name == "admin_1.py":
        return '''import streamlit as st

st.header("Admin 1")
st.write(f"You are logged in as {st.session_state.role}.")
'''
    
    # Default template for Python files
    return f'''import streamlit as st

st.title(f"{dir_name}/{file_name}")
'''

def create_structure(base_path: str, items: List[Union[str, Dict]], complete_structure: dict, dry_run: bool = False) -> None:
    """Create directory structure based on parsed YAML content."""
    for item in items:
        if isinstance(item, str):
            file_path = os.path.join(base_path, item)
            if not dry_run:
                if not os.path.exists(file_path):
                    content = create_file_content(
                        file_path=file_path,
                        dir_name=os.path.basename(base_path),
                        file_name=item,
                        complete_structure=complete_structure
                    )
                    with open(file_path, 'w') as f:
                        f.write(content)
                    click.echo(f"Created file: {file_path}")
                else:
                    click.echo(f"File already exists: {file_path}")
            else:
                click.echo(f"[DRY RUN] Would create file: {file_path}")
        
        elif isinstance(item, dict):
            for dir_name, contents in item.items():
                dir_path = os.path.join(base_path, dir_name)
                if not dry_run:
                    os.makedirs(dir_path, exist_ok=True)
                click.echo(f"{'[DRY RUN] ' if dry_run else ''}Created directory: {dir_path}")
                
                if isinstance(contents, list):
                    create_structure(dir_path, contents, complete_structure, dry_run)
                elif isinstance(contents, dict):
                    for subdir, subcontents in contents.items():
                        subdir_path = os.path.join(dir_path, subdir)
                        if not dry_run:
                            os.makedirs(subdir_path, exist_ok=True)
                        click.echo(f"{'[DRY RUN] ' if dry_run else ''}Created directory: {subdir_path}")
                        create_structure(
                            subdir_path,
                            subcontents if isinstance(subcontents, list) else [subcontents],
                            complete_structure,
                            dry_run
                        )

@click.group()
def cli():
    """CLI tool to create directory structure from YAML files."""
    pass

@cli.command()
@click.argument('yaml_file', type=click.Path(exists=True))
@click.option('--dry-run', is_flag=True, help='Print actions without creating files/directories')
@click.option('--output-dir', '-o', type=str, help='Custom output directory name')
def create(yaml_file: str, dry_run: bool, output_dir: Optional[str]) -> None:
    """Create directory structure from YAML file."""
    try:
        with open(yaml_file, 'r') as file:
            structure = yaml.safe_load(file)
        
        if not structure:
            raise click.ClickException("YAML file is empty or invalid")
        
        yaml_root_dir = list(structure.keys())[0]
        root_dir = output_dir if output_dir else get_default_output_dir(yaml_file)
        
        # Create root directory
        if not dry_run:
            os.makedirs(root_dir, exist_ok=True)
        click.echo(f"{'[DRY RUN] ' if dry_run else ''}Created root directory: {root_dir}")
        
        # Create structure with access to complete YAML structure
        create_structure(root_dir, structure[yaml_root_dir], structure, dry_run)
        
        click.echo(click.style("\nDirectory structure created successfully!", fg="green"))
        
    except yaml.YAMLError as e:
        raise click.ClickException(f"Error parsing YAML file: {e}")
    except Exception as e:
        raise click.ClickException(str(e))

@cli.command()
@click.argument('yaml_file', type=click.Path(exists=True))
def validate(yaml_file: str) -> None:
    """Validate YAML file structure without creating directories."""
    try:
        with open(yaml_file, 'r') as file:
            structure = yaml.safe_load(file)
        
        if not structure:
            raise click.ClickException("YAML file is empty")
        
        root_dir = list(structure.keys())[0]
        if not isinstance(structure[root_dir], list):
            raise click.ClickException("Invalid structure: root must contain a list of items")
        
        click.echo(click.style("YAML file is valid!", fg="green"))
        click.echo(f"Root directory will be: {get_default_output_dir(yaml_file)}")
        
    except yaml.YAMLError as e:
        raise click.ClickException(f"Invalid YAML syntax: {e}")
    except Exception as e:
        raise click.ClickException(str(e))

if __name__ == "__main__":
    cli()