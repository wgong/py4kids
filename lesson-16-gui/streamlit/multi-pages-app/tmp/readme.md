
## streamlit create
https://claude.ai/chat/5cf51280-3957-4099-abc3-c517d9b7f64f

## usage

```

root-folder/
├── readme.md
├── app.py
├── images/
    ├── icon_1.png
    └── icon_2.png
├── src
    ├── settings.py
    ├── admin/
    │   ├── admin_1.py
    │   └── admin_2.py
    ├── request/
    │   ├── request_1.py
    │   └── request_2.py
    └── respond/
        ├── respond_1.py
        └── respond_2.py



python st_create_project-v3.py create ex5.yaml --dry-run

python st_create_project-v3.py create ex5.yaml


# Using YAML filename as directory name (example-4.yaml -> example-4)
python st_create_project.py create example-4.yaml --dry-run

# Using custom output directory
python st_create_project.py create example-4.yaml --output-dir custom-name

# Validate and see what the default directory name would be
python st_create_project.py validate example-4.yaml

```