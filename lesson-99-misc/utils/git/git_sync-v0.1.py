import os
import subprocess
import yaml

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
        print(f"Error loading config file: {e}")
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
        print(f"Error running command '{' '.join(command)}' in {repo_path}: {e.stderr}")
        return None

def sync_repo(repo_path):
    """
    Sync a single repository:
    1. Fetch the latest changes from the remote.
    2. Pull the latest changes if possible.
    3. Check the status to see if there are local changes to push.
    4. Add, commit, and push changes if there are any local modifications.
    """
    print(f"\nProcessing repository: {repo_path}")
    
    # Step 1: Fetch the latest changes from the remote
    print("Fetching latest changes...")
    fetch_output = run_git_command(repo_path, ['git', 'fetch'])
    if fetch_output is not None:
        print(fetch_output.strip())
    
    # Step 2: Pull the latest changes
    print("Pulling latest changes...")
    pull_output = run_git_command(repo_path, ['git', 'pull'])
    if pull_output is not None:
        print(pull_output.strip())
    
    # Step 3: Check the status for any local changes
    print("Checking status...")
    status_output = run_git_command(repo_path, ['git', 'status'])
    if status_output is not None:
        print(status_output.strip())
    
    # Step 4: If there are changes, stage, commit, and push them
    if "nothing to commit" not in status_output:
        print("Local changes detected. Staging, committing, and pushing changes...")
        
        # Stage all changes
        add_output = run_git_command(repo_path, ['git', 'add', '.'])
        if add_output is not None:
            print("Staged all changes.")
        
        # Commit with a dummy message
        commit_output = run_git_command(repo_path, ['git', 'commit', '-m', 'update'])
        if commit_output is not None:
            print("Committed changes with message 'update'.")
        
        # Push changes to the remote
        push_output = run_git_command(repo_path, ['git', 'push'])
        if push_output is not None:
            print("Pushed changes to the remote.")
    else:
        print("No local changes to push.")

def main():
    # Path to the YAML configuration file
    config_file = 'git_sync_config.yaml'
    
    # Load the list of repositories from the config file
    repos = load_config(config_file)
    if not repos:
        print("No repositories found in the config file.")
        return
    
    # Iterate through each repository and sync it
    for repo in repos:
        repo_path = repo.get('path')
        if not repo_path or not os.path.isdir(repo_path):
            print(f"Invalid or missing repository path: {repo_path}")
            continue
        
        sync_repo(repo_path)

if __name__ == "__main__":
    main()