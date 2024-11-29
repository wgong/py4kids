from pathlib import Path

def create_folder_structure():
    # Root directory
    root = Path('csv-import-app')
    root.mkdir(exist_ok=True)

    # Frontend structure
    frontend = root / 'frontend'
    frontend.mkdir(exist_ok=True)
    
    # Frontend subdirectories and files
    (frontend / 'public').mkdir(exist_ok=True)
    (frontend / 'src').mkdir(exist_ok=True)
    (frontend / 'src' / 'components').mkdir(exist_ok=True)
    
    # Create frontend files
    (frontend / 'src' / 'components' / 'CSVImportApp.jsx').touch()
    (frontend / 'src' / 'App.jsx').touch()
    (frontend / 'src' / 'index.jsx').touch()
    (frontend / 'package.json').touch()
    (frontend / '.env').touch()

    # Backend structure
    backend = root / 'backend'
    backend.mkdir(exist_ok=True)
    
    # Backend subdirectories
    app_dir = backend / 'app'
    app_dir.mkdir(exist_ok=True)
    
    # Create backend files
    (app_dir / '__init__.py').touch()
    (app_dir / 'main.py').touch()
    (app_dir / 'utils.py').touch()
    (backend / 'requirements.txt').touch()
    (backend / '.env').touch()
    
    # Create README
    (root / 'README.md').touch()

    # Add comments to specific files
    files_with_comments = {
        frontend: '# React frontend',
        backend: '# FastAPI backend',
        app_dir / 'main.py': '# FastAPI application',
        app_dir / 'utils.py': '# Utility functions'
    }
    
    for file_path, comment in files_with_comments.items():
        if file_path.is_file():
            with open(file_path, 'w') as f:
                f.write(comment)
        else:
            # For directories, create a .info file with the comment
            with open(file_path / '.info', 'w') as f:
                f.write(comment)

if __name__ == '__main__':
    create_folder_structure()
    print("Folder structure created successfully!")