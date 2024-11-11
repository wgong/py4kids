
# [Homepage](https://pandas-ai.com/)

Ask questions to your company data in natural language. PandasAI empowers decision-makers with instant, data-driven insights, enhancing productivity and informed decision-making.

PandasAI uses a generative AI model to understand and interpret natural language queries and translate them into python code and SQL queries. It then uses the code to interact with the data and return the results to the user.

# [Documentation](https://docs.pandas-ai.com/index)

## Blogs
- [PandasAI: Simplifying Data Analysis through Generative AI](https://medium.com/@soumava.dey.aig/pandasai-simplifying-data-analysis-through-generative-ai-980b73a410ff)



## GitHub

# [Source Code](https://github.com/Sinaptik-AI/pandas-ai)

# Tutorials

## Setup
get API Key at https://www.pandabi.ai/admin/api-keys
```

conda create -n pandasai python=3.11
conda activate pandasai
pip install pandasai notebook
pip install pandasai[connectors]
pip install yfinance

```

## Quick Start

```
from api_key_store import ApiKeyStore
import os
s = ApiKeyStore()
os.environ["PANDASAI_API_KEY"] = s.get_api_key(provider="PANDASAI") 
```


## Examples

- [Examples](https://docs.pandas-ai.com/examples)
- [PandasAI, OpenAI and Streamlit - Analyzing File Uploads with User Prompts](https://www.youtube.com/watch?v=oSC2U2iuMRg)
- [PandasAI: AI Copilot for Your Data - Excel, MySQL, BigQuery, and More](https://www.youtube.com/watch?v=sNrGanuranQ)

<span style="color:red">recommended by </span>


# What's Next

## Projects

### 
