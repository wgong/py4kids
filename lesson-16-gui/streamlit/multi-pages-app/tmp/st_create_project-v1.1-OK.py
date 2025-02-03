import os
import yaml
import click
from pathlib import Path
from typing import Optional, Union, List, Dict

def get_default_output_dir(yaml_file: str) -> str:
    """Extract default output directory name from YAML filename."""
    return Path(yaml_file).stem

def create_structure(base_path: str, items: List[Union[str, Dict]], dry_run: bool = False) -> None:
    """
    Create directory structure based on parsed YAML content.
    
    Args:
        base_path (str): Base directory path
        items (List): List of items (files or directories)
        dry_run (bool): If True, only print actions without creating files/directories
    """
    for item in items:
        if isinstance(item, str):
            # Handle file
            file_path = os.path.join(base_path, item)
            if not dry_run:
                if not os.path.exists(file_path):
                    Path(file_path).touch()
                    click.echo(f"Created file: {file_path}")
                else:
                    click.echo(f"File already exists: {file_path}")
            else:
                click.echo(f"[DRY RUN] Would create file: {file_path}")
        
        elif isinstance(item, dict):
            # Handle directory
            for dir_name, contents in item.items():
                dir_path = os.path.join(base_path, dir_name)
                if not dry_run:
                    os.makedirs(dir_path, exist_ok=True)
                click.echo(f"{'[DRY RUN] ' if dry_run else ''}Created directory: {dir_path}")
                
                if isinstance(contents, list):
                    # Handle files in directory
                    create_structure(dir_path, contents, dry_run)
                elif isinstance(contents, dict):
                    # Handle nested directories
                    for subdir, subcontents in contents.items():
                        subdir_path = os.path.join(dir_path, subdir)
                        if not dry_run:
                            os.makedirs(subdir_path, exist_ok=True)
                        click.echo(f"{'[DRY RUN] ' if dry_run else ''}Created directory: {subdir_path}")
                        create_structure(subdir_path, subcontents if isinstance(subcontents, list) else [subcontents], dry_run)

@click.group()
def cli():
    """CLI tool to create directory structure from YAML files."""
    pass

@cli.command()
@click.argument('yaml_file', type=click.Path(exists=True))
@click.option('--dry-run', is_flag=True, help='Print actions without creating files/directories')
@click.option('--output-dir', '-o', type=str, help='Custom output directory name')
def create(yaml_file: str, dry_run: bool, output_dir: Optional[str]) -> None:
    """Create directory structure from YAML file.
    
    YAML_FILE: Path to the YAML file containing directory structure
    """
    try:
        # Read YAML file
        with open(yaml_file, 'r') as file:
            structure = yaml.safe_load(file)
        
        if not structure:
            raise click.ClickException("YAML file is empty or invalid")
        
        # Get the root directory name from YAML
        yaml_root_dir = list(structure.keys())[0]
        
        # Determine output directory
        root_dir = output_dir if output_dir else get_default_output_dir(yaml_file)
        
        # Create root directory
        if not dry_run:
            os.makedirs(root_dir, exist_ok=True)
        click.echo(f"{'[DRY RUN] ' if dry_run else ''}Created root directory: {root_dir}")
        
        # Create the structure inside root directory
        create_structure(root_dir, structure[yaml_root_dir], dry_run)
        
        click.echo(click.style("\nDirectory structure created successfully!", fg="green"))
        
    except yaml.YAMLError as e:
        raise click.ClickException(f"Error parsing YAML file: {e}")
    except Exception as e:
        raise click.ClickException(str(e))

@cli.command()
@click.argument('yaml_file', type=click.Path(exists=True))
def validate(yaml_file: str) -> None:
    """Validate YAML file structure without creating directories.
    
    YAML_FILE: Path to the YAML file to validate
    """
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