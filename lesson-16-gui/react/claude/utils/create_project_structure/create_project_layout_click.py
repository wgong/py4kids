"""
$ python create_project_layout.py layout.md --output ./my-project
"""

from pathlib import Path
from typing import Optional
import re
import click


def is_likely_file(name):
    # Common file patterns
    file_patterns = [
        r'\.[a-zA-Z0-9]+$',  # Has extension
        r'^\.env$',          # Dot files
        r'\.md$',           # Markdown files
        r'package\.json$',   # Special files
        r'^__init__\.py$'    # Python init
    ]
    return any(re.search(pattern, name) for pattern in file_patterns)

def parse_layout(md_file):
    structure = {}
    current_path = []
    previous_level = -1
    
    with open(md_file) as f:
        lines = [line.rstrip() for line in f.readlines() if line.strip()]
        
        for i, line in enumerate(lines):
            indent = len(line) - len(line.lstrip())
            level = indent // 4
            
            # Adjust current path based on level
            current_path = current_path[:level]
            
            # Extract name and comment
            parts = line.strip().split('#', 1)
            name = parts[0].strip('- ').strip()
            comment = parts[1].strip() if len(parts) > 1 else ''
            
            # Determine if item is a file or directory
            is_file = False
            if is_likely_file(name):
                is_file = True
            elif i < len(lines) - 1:  # Check next line's indentation
                next_indent = len(lines[i + 1]) - len(lines[i + 1].lstrip())
                if next_indent <= indent:  # No children, likely a file
                    is_file = True
            
            # Build path and store with type information
            current_path.append(name)
            path_key = '/'.join(current_path)
            structure[path_key] = {
                'is_file': is_file,
                'comment': comment
            }
            
            previous_level = level
    
    return structure

def create_structure(structure, output_dir):
    out_dir = Path(output_dir) 

    # Get root directory from first path
    root = out_dir / Path(next(iter(structure)).split('/')[0])
    root.mkdir(exist_ok=True)
    
    # Create all directories and files
    for path, info in structure.items():
        full_path = out_dir / Path(path)
        if info['is_file']:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.touch()
        else:
            full_path.mkdir(parents=True, exist_ok=True)
    
    # Add comments
    for path, info in structure.items():
        if not info['comment']:
            continue
            
        full_path = out_dir / Path(path)
        if info['is_file']:
            with open(full_path, 'w') as f:
                f.write(f"# {info['comment']}")
        else:
            with open(full_path / '.info', 'w') as f:
                f.write(info['comment'])


@click.command(help="Create project folder structure from markdown layout file")
@click.argument('layout_file', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('--output', '-o', type=click.Path(path_type=Path), help="Output directory")
def create(layout_file: Path, output: Optional[Path]):
    """Create folder structure from markdown layout file."""
    try:
        structure = parse_layout(layout_file)
        output_dir = output or Path.cwd()
        create_structure(structure, output_dir)
        click.echo(f"✓ Folder structure created in {output_dir}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Exit(1)

if __name__ == "__main__":
    create()