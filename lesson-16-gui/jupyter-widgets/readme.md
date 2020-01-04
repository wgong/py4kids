## The Jupyter Widget Ecosystem - SciPy 2019 Tutorial
https://github.com/wgong/tutorial 
    * fork of https://github.com/jupyter-widgets/tutorial
    * ~/projects/JupyterCookbook/tutorial

### Conda installation
```
conda create -n widgets-tutorial -c conda-forge python=3.7 pip notebook numpy scikit-image scipy pandas requests ipywidgets bqplot ipyvolume ipyleaflet pythreejs ipyevents ipysheet ipytree ipympl pywwt voila=0.1 jupyterlab nodejs=11.14

conda activate widgets-tutorial

# Install ipyvuetify and voila-vuetify from pip (not on conda-forge yet)
pip install ipyvuetify voila-vuetify

# Create a kernel for this environment
ipython kernel install --name widgets-tutorial --display-name widgets-tutorial --sys-prefix

# Enable JupyterLab extensions, which may take several minutes
jupyter labextension install @jupyter-widgets/jupyterlab-manager bqplot ipyvolume jupyter-threejs jupyter-leaflet ipysheet ipytree jupyter-matplotlib jupyter-vuetify

$ python install_check.py

Checking requirements for Jupyter widget ecosystem...........
	All required packages installed
Checking voila version:
0.1.20
	Voila is correctly installed
Checking version numbers of these packages:  ipywidgets, notebook, jupyterlab
	ipywidgets version is good!

**** Please upgrade notebook to version 5.7 by running:
        conda install notebook=5.7 # if you use conda
        pip install notebook==5.7

**** Please upgrade jupyterlab to version 1.0 by running:
        conda install jupyterlab=1.0 # if you use conda
        pip install jupyterlab==1.0
Checking whether kernel widgets-tutorial exists
	Custom kernel is correctly installed

```



## PyViz
[PyViz: Dashboards for Visualizing 1 Billion Datapoints in 30 Lines of Python](https://youtu.be/k27MJJLJNT4)