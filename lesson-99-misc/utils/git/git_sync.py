"""
Git Sync Script

This Python script automates the process of synchronizing multiple Git repositories 
based on a YAML configuration file. It performs the following tasks for each repository:

1. Fetches the latest changes from the remote server.
2. Pulls the latest changes into the local branch.
3. Checks the status of the repository to identify any local changes.
4. If local changes are detected:
   - Stages all changes (`git add .`).
   - Commits the changes with a dummy message ("update").
   - Pushes the changes to the remote repository.

The script uses the `click` library to provide a user-friendly CLI interface and supports 
a default configuration file located at `~/git_sync_config.yaml`. You can also specify a 
custom configuration file using the `--config` option.

Configuration File Format:
    repos:
      - path: /path/to/repo1
      - path: /path/to/repo2

Usage:
    python git_sync.py
    python git_sync.py --config /path/to/custom_config.yaml
    python git_sync.py --help

Options:
    -c, --config PATH  Path to the YAML configuration file (default: ~/git_sync_config.yaml).
    --help             Show this message and exit.

Dependencies:
    - PyYAML: For reading the YAML configuration file.
    - Click: For creating the CLI interface.

Installation:
    pip install pyyaml click

Example Configuration File (~/git_sync_config.yaml):
    repos:
      - path: /home/papagame/projects/wgong/phidata
      - path: /home/papagame/projects/digital-duck/zinets

Author:
    Your Name <your_email@example.com>
"""

import os
import subprocess
import yaml
import click

def load_config(config_file):
    """
    Load the YAML configuration file containing the list of repositories.
    Expected format:
        repos:
          - path: /path/to/repo1
          - path: /path/to/repo2
    """
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config.get('repos', [])
    except Exception as e:
        click.echo(f"Error loading config file: {e}", err=True)
        return []

def run_git_command(repo_path, command):
    """
    Run a Git command in the specified repository directory.
    """
    try:
        result = subprocess.run(
            command,
            cwd=repo_path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        click.echo(f"Error running command '{' '.join(command)}' in {repo_path}: {e.stderr}", err=True)
        return None

def parse_git_status(status_output):
    """
    Parse the output of `git status` to extract changed files.
    Returns a dictionary with lists of modified, added, and deleted files.
    """
    changes = {
        "modified": [],
        "added": [],
        "deleted": []
    }
    lines = status_output.splitlines()
    for line in lines:
        if "modified:" in line:
            changes["modified"].append(line.strip().split("modified:")[1].strip())
        elif "new file:" in line:
            changes["added"].append(line.strip().split("new file:")[1].strip())
        elif "deleted:" in line:
            changes["deleted"].append(line.strip().split("deleted:")[1].strip())
    return changes

def sync_repo(repo_path):
    """
    Sync a single repository:
    1. Fetch the latest changes from the remote.
    2. Pull the latest changes if possible.
    3. Check the status to see if there are local changes to push.
    4. Add, commit, and push changes if there are any local modifications.
    """
    click.echo(click.style(f"\nProcessing repository: {repo_path}", fg="cyan", bold=True))
    
    # Step 1: Fetch the latest changes from the remote
    click.echo("Fetching latest changes...")
    fetch_output = run_git_command(repo_path, ['git', 'fetch'])
    if fetch_output is not None:
        click.echo(fetch_output.strip())
    
    # Step 2: Pull the latest changes
    click.echo("Pulling latest changes...")
    pull_output = run_git_command(repo_path, ['git', 'pull'])
    if pull_output is not None:
        click.echo(pull_output.strip())
    
    # Step 3: Check the status for any local changes
    click.echo("Checking status...")
    status_output = run_git_command(repo_path, ['git', 'status'])
    if status_output is not None:
        click.echo(status_output.strip())
    
    # Parse the status output to extract changed files
    changes = parse_git_status(status_output)
    
    # Highlight changed files
    if changes["modified"]:
        click.echo(click.style("\nModified files:", fg="yellow", bold=True))
        for file in changes["modified"]:
            click.echo(click.style(f"  {file}", fg="yellow"))
    if changes["added"]:
        click.echo(click.style("\nNew files:", fg="green", bold=True))
        for file in changes["added"]:
            click.echo(click.style(f"  {file}", fg="green"))
    if changes["deleted"]:
        click.echo(click.style("\nDeleted files:", fg="red", bold=True))
        for file in changes["deleted"]:
            click.echo(click.style(f"  {file}", fg="red"))
    
    # Step 4: If there are changes, stage, commit, and push them
    if "nothing to commit" not in status_output:
        click.echo(click.style("\nLocal changes detected. Staging, committing, and pushing changes...", fg="cyan"))
        
        # Stage all changes
        add_output = run_git_command(repo_path, ['git', 'add', '.'])
        if add_output is not None:
            click.echo(click.style("Staged all changes.", fg="green"))
        
        # Commit with a dummy message
        commit_output = run_git_command(repo_path, ['git', 'commit', '-m', 'update'])
        if commit_output is not None:
            click.echo(click.style("Committed changes with message 'update'.", fg="green"))
        
        # Push changes to the remote
        push_output = run_git_command(repo_path, ['git', 'push'])
        if push_output is not None:
            click.echo(click.style("Pushed changes to the remote.", fg="green"))
    else:
        click.echo(click.style("No local changes to push.", fg="blue"))

@click.command()
@click.option('--config', '-c', default=os.path.expanduser('~/git_sync_config.yaml'),
              help='Path to the YAML configuration file (default: ~/git_sync_config.yaml).')
def main(config):
    """
    Synchronize multiple Git repositories based on a YAML configuration file.

    The configuration file should contain a list of repositories with their paths.
    Example:
        repos:
          - path: /path/to/repo1
          - path: /path/to/repo2
    """
    click.echo(f"Using configuration file: {config}")
    
    # Load the list of repositories from the config file
    repos = load_config(config)
    if not repos:
        click.echo("No repositories found in the config file.", err=True)
        return
    
    # Iterate through each repository and sync it
    for repo in repos:
        repo_path = repo.get('path')
        if not repo_path or not os.path.isdir(repo_path):
            click.echo(f"Invalid or missing repository path: {repo_path}", err=True)
            continue
        
        sync_repo(repo_path)

if __name__ == "__main__":
    main()