### Docs
https://microsoft.github.io/autogen/dev//user-guide/agentchat-user-guide/magentic-one.html


- [User-Guide](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/magentic-one.html)

### Source 
~/projects/wgong/autogen

### Setup 

```
conda create -n ag python=3.11
conda activate ag

pip install "autogen-agentchat" "autogen-ext[magentic-one,openai]" "autogen_ext" "tiktoken"

# If using the MultimodalWebSurfer, you also need to install playwright dependencies:
playwright install --with-deps chromium


```

- [Get started](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/magentic-one.html#getting-started)


### Tutorial

```
cd py4kids/lesson-18-ai/Agents/autogen/magnetic-one

pip install -U "autogen-ext[ollama]"

```
