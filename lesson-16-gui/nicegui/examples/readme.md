## icons

Create a NiceGui app to display Google Material Design Icons

### Collect icon names

Because Icon names at https://fonts.google.com/icons can not be scraped by Beautifulsoup possibly due to Google policy, I found its github at https://github.com/google/material-design-icons. Download the repo to a local folder and unzip. This repo size is large at 3.6 GB.

One collect the icon names by walking the source tree at `material-design-icons-master/src` folder, they are organized by category.

After running [this jupyter notebook](https://github.com/wgong/py4kids/blob/master/lesson-16-gui/nicegui/examples/icons/walk_tree_at_fixed_depth.ipynb), I save icon names into a CSV file, and generate `main.py` [script](https://github.com/wgong/py4kids/blob/master/lesson-16-gui/nicegui/examples/icons/main.py) for NiceGui

### Run NiceGui app

```
$ pip install nicegui
$ python main.py
```