
# AG2 (AutoGen - community edition)

- [Docs](https://docs.ag2.ai/docs/Home)
- [Blogs](https://docs.ag2.ai/docs/blog/2025-02-13-DeepResearchAgent/index)


## Goal - Agentic RAG
Build Data Copilot on Agentic RAG framework

## Local Dev

```bash
conda env remove --name agent
conda clean --all  # remove unused env space

conda create -n ag2 python=3.11
conda activate ag2

# my forked
cd ~/projects/wgong/AG2

git clone git@github.com:wgong/ag2.git
git clone git@github.com:wgong/build-with-ag2.git

cd ag2
pip install -e ".[openai,rag]"   # use DocAgent
pip install ag2==0.8.0b1

# Also delete the cache
rm -rf notebook/.cache

# notes
# see ~/projects/wgong/AG2/ag2/notebook/u8hi_agents/readme.md


# original
cd ~/projects/AI/

git clone git@github.com:ag2ai/ag2.git

# old work
git clone git@github.com:wgong/autogen.git
```

## Tutorials

### AI Agentic Design Patterns with AutoGen
- https://www.youtube.com/watch?v=TBNTH-fwGPE
- ~/projects/wgong/py4kids/lesson-18-ai/Agents/autogen/agentic-design-patterns/notebooks

### DocAgent
- [Video](https://www.youtube.com/watch?v=sNKQR4LNOK0&t=1s)
- [Doc](https://docs.ag2.ai/docs/user-guide/reference-agents/docagent)

- ~/projects/wgong/AG2/ag2/notebook/agents_docagent_u8hi.ipynb
    - Issues
        - https://github.com/ag2ai/ag2/issues/1167

#### Setup
```
pip install ag2[rag]

cd ~/projects/wgong/AG2/ag2

# ~/projects/wgong/AG2/ag2/notebook/agents_docagent.ipynb
```




## Research

### Claude 

- [AgenticRAG](https://claude.ai/chat/a4d58084-8e60-497b-9f79-82e3c8c953e8)

### DeepSeek

- [AgenticRAG](https://chat.deepseek.com/a/chat/s/afd1e47d-ea07-4c88-8fac-096c4d903b39)

### Gemini 2.0 Advanced

- [AgenticRAG](https://gemini.google.com/app/eed42f92e68ed902)

## Releases

- [v0.7](https://www.linkedin.com/posts/chi-wang-autogen_ag2-agentos-ai-activity-7285060224976044032--yWH/?utm_source=social_share_send&utm_medium=android_app&utm_campaign=share_via)


## Microsoft

### AutoGen (original)

```
cd ~/projects/AI/Microsoft/

git clone git@github.com:microsoft/autogen.git

```



### TaskWeaver

```
cd ~/projects/AI/Microsoft/

git clone git@github.com:wgong/TaskWeaver.git

```
