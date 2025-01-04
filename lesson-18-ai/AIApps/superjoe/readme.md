https://claude.ai/chat/3883912c-bae6-4f82-85de-2f09382f1c90



```
conda create -n rag python=3.11
conda activate rag
pip install -r requirements.txt

```


### TMP


query_results = collection.query(
    query_texts=["Teach me about music history"],
    where={"genre": {"$in": ["music", "history"]}},
    n_results=2,
)

query_results["documents"], query_results["distances"]
[
  [
    "Beethoven's Symphony No. 9 is celebrated for its powerful choral finale, 'Ode to Joy.'",
    'The American Revolution had a profound impact on the birth of the United States as a nation.'
  ]
]

