
# Additional Notes
- [plotly 5.23.0 is incompatible with vanna 0.7.4](https://github.com/vanna-ai/vanna/issues/704)


## GPU selection
see [Ollama GPU docs](https://github.com/ollama/ollama/blob/main/docs%2Fgpu.md)

```
nvidia-smi      # see GPU memory info
nvidia-smi -L   # see GPU UUID
```

### GPU Suspend/Resume
After Linux suspect, sometimes Ollama will fail to discover your NVIDIA GPU, and fallback to running on the CPU.

To workaround this driver bug by reloading the NVIDIA UVM driver with 
```
sudo rmmod nvidia_uvm && sudo modprobe nvidia_uvm
```

To off-load all models in use, restart ollama service
```
sudo systemctl restart ollama
nvidia-smi      # see GPU memory info
```

## AWS Bedrock

### quick start
https://github.com/build-on-aws/amazon-bedrock-quick-start

## Feature Roadmap

- add auth (register/login) 
    - see `habits7`

- add access to resources 
    - t_user
    - t_resource (DB/LLM)
        - 1st user owns the added resource
        - other user request access to the resource, approved by owner
    - t_user_resource (intersection) similar to IAM Role

- add rate limit based on pricing plan
    - demo (chinook/gpt-3.5-turbo)
    - developer
    - team
    - org

- add more data types/sources 

- chat with docs (PDF, text, ...)

- RAG on/off

- allows user to manage app data, knowledge data
    - import
    - export

- SaaS integrations
    - example: https://raizuum.onrender.com/ (https://discuss.streamlit.io/t/my-saas-is-100-streamlit-and-it-survived-1000-connected-users-and-4months-without-a-service-fail/86177) 
    - payment service (stripe)
    - email service (mailJet)
    - usage metrics (Statcounter)

- manage task

- manage note

- BI on data (task, note, user, resource, knowledge)
    - recommender
    - dashboard
    - report



## Change Logs

- [2024-08-03] add IMDB movie dataset
evaluate the same questions as asked in https://www.kaggle.com/code/priy998/imdb-sqlite/notebook

- [2024-07-21] upgrade Vanna from `0.6.2` to `0.6.3` to support AWS Bedrock