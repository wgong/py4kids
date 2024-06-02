# Vanna.AI Streamlit App
<img width="1392" alt="Screenshot 2023-06-23 at 3 49 45 PM" src="./assets/vanna_demo.gif">

# Install

```bash
conda create -n vanna python=3.11
conda activate vanna
pip install -r requirements.txt
```

# Configure
Modify the `setup_vanna` function in [vanna_calls.py](./vanna_calls.py) to use your desired Vanna setup as follows.

```
class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

@st.cache_resource(ttl=3600)
def setup_vanna():

    config = {
        'model': 'llama3',
    }
    vn = MyVanna(config=config)
    file_db = "~/Downloads/chinook.sqlite"
    vn.connect_to_sqlite(file_db)

    return vn

```

SQLite sample database `chinook.sqlite` is stored in `~/Downloads/`

Local LLM `llama3` is used via `Ollama` framework.

You can configure secrets in `.streamlit/secrets.toml` and access them in your app using `st.secrets.get(...)`.

# Run

```bash
streamlit run app.py
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
