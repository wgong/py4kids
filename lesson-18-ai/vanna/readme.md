
# Intro

Vanna is a Python package that uses retrieval augmentation to help you generate accurate SQL queries for your database using LLMs.


# Resources

## [Homepage](https://vanna.ai/)

## [Documentation](https://vanna.ai/docs/)

### Blogs
- [Vanna AI](https://medium.com/vanna-ai)
    - [SQL Copilot](https://medium.com/vanna-ai/intro-to-vanna-a-python-based-ai-sql-co-pilot-218c25b19c6a)

## [Source](https://github.com/vanna-ai/vanna)

## Tutorial






### Local
- ~/projects/AI/lighthouse-learning-machine/data-analyst/vanna

- ~/projects/AI/lighthouse-learning-machine/data-analyst/notebooks/sqlite-ollama-chromadb-u1gwg.ipynb





## Install
```bash
cd ~/projects/AI/lighthouse-learning-machine/data-analyst/vanna
conda create -n vanna python=3.11
conda activate vanna
pip install vanna notebook

```

## Demos


### Sync source
- cd ~/projects/AI/lighthouse-learning-machine/data-analyst/notebooks
- git pull

- conda activate vanna
- pip install vanna
- pip install 'vanna[chromadb]'

### jupyter notebook
- clone one from <SQL-DB>-<LLM>-<VectorDB>.ipynb by adding `-u1gwg` suffix and copy it to `demo` sub-folder
- run
- save it as .html into `demo` folder for reference 


### Streamlit

Got the following error when running flask from within Jupyter notebook: 
```
zmq.error.ZMQError: Address already in use (addr='tcp://127.0.0.1:59961')
An exception has occurred, use %tb to see the full traceback.
```
see https://github.com/vanna-ai/vanna/issues/398

Suggest to run standalone Flask/Streamlit app 
