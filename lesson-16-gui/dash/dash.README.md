### [Dash GitHub](https://github.com/plotly/dash)

### [Dash Sample Apps](https://github.com/plotly/dash-sample-apps)


#### How to run a Dash Sample app
$ cd ~/projects/Dash/dash-sample-apps
$ python -m venv dashvenv
$ source dashvenv/bin/activate
$ cd dash-brain-viewer/
$ pip install -r requirements.txt 
$ python app.py
open url=http://127.0.0.1:8050/ in browser



###  jupyter-dash : Dash in Jupyter Notebook
- `pip install jupyter-dash`
- edit dash `app.py` to `app.ipynb`
    - add `import jupyter_dash`
    - replace `dash` with `jupyter_dash`
    - replace `Dash` with `JupyterDash`
    - add `mode="inline" or "external" (default)` to app.run_server()


### install Dash
$ pip install dash
$ pip list | grep dash
dash                               1.2.0    
dash-core-components               1.1.2    
dash-html-components               1.0.1    
dash-renderer                      1.0.1    
dash-table                         4.2.0   

$ pip list | grep plotly
plotly                             4.1.0    


cd /home/gong/projects/Dash/datacamp
-- cd /home/devopsgong/dash/datacamp

* create app.py

* python app.py
 a new web server at http://127.0.0.1:8050/

 [Pusher](https://pusher.com/tutorials/live-dashboard-python)


### Plotly.Express

https://medium.com/plotly/introducing-plotly-express-808df010143d

please review this medium article:
https://medium.com/plotly/introducing-plotly-express-808df010143d
It is the simplest way to visualize data in python so far I have seen
The walkthru notebook is at https://nbviewer.jupyter.org/github/plotly/plotly_express/blob/gh-pages/walkthrough.ipynb

If one wants to build Dashboard to demo data or allow others to explore data,
Dash (same plotly python syntax) is a web app
Here is gallery of sample apps one can borrow and customize
https://dash-gallery.plotly.host/Portal/


### Documentations

- [Dash-by-Plotly](https://github.com/Coding-with-Adam/Dash-by-Plotly)

- [Dash for Beginners](https://www.datacamp.com/community/tutorials/learn-build-dash-python)

- [Our World in Data](https://ourworldindata.org/)
    - https://github.com/owid



