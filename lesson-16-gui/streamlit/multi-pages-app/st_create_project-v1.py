import os
import yaml
import click
from pathlib import Path
from typing import Optional

def get_default_output_dir(yaml_file: str) -> str:
    """Extract default output directory name from YAML filename."""
    # Get filename without extension and path
    return Path(yaml_file).stem

def create_structure(structure: dict, root_dir: str, dry_run: bool = False) -> None:
    """
    Create directory structure based on parsed YAML content.
    
    Args:
        structure (dict): Parsed YAML content
        root_dir (str): Root directory name
        dry_run (bool): If True, only print actions without creating files/directories
    """
    # Create root directory
    if not dry_run:
        os.makedirs(root_dir, exist_ok=True)
    click.echo(f"{'[DRY RUN] ' if dry_run else ''}Created root directory: {root_dir}")
    
    # Process subdirectories and files
    for subdir, files in structure[root_dir].items():
        # Create full path for subdirectory
        subdir_path = os.path.join(root_dir, subdir)
        if not dry_run:
            os.makedirs(subdir_path, exist_ok=True)
        click.echo(f"{'[DRY RUN] ' if dry_run else ''}Created subdirectory: {subdir_path}")
        
        # Create files in subdirectory
        if isinstance(files, list):
            for file_name in files:
                file_path = os.path.join(subdir_path, file_name)
                if not dry_run:
                    if not os.path.exists(file_path):
                        Path(file_path).touch()
                        click.echo(f"Created file: {file_path}")
                    else:
                        click.echo(f"File already exists: {file_path}")
                else:
                    click.echo(f"[DRY RUN] Would create file: {file_path}")

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
        
        # Determine output directory:
        # 1. Use --output-dir if provided
        # 2. Otherwise use YAML filename without extension
        root_dir = output_dir if output_dir else get_default_output_dir(yaml_file)
        
        # Restructure with new root directory name
        structure = {root_dir: structure[yaml_root_dir]}
        
        create_structure(structure, root_dir, dry_run)
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
        if not isinstance(structure[root_dir], dict):
            raise click.ClickException("Invalid structure: root must contain subdirectories")
        
        click.echo(click.style("YAML file is valid!", fg="green"))
        click.echo(f"Root directory will be: {get_default_output_dir(yaml_file)}")
        
    except yaml.YAMLError as e:
        raise click.ClickException(f"Invalid YAML syntax: {e}")
    except Exception as e:
        raise click.ClickException(str(e))

if __name__ == "__main__":
    cli()