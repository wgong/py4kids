
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


## Change Logs

- [2024-08-03] add IMDB movie dataset
evaluate the same questions as asked in https://www.kaggle.com/code/priy998/imdb-sqlite/notebook

- [2024-07-21] upgrade Vanna from `0.6.2` to `0.6.3` to support AWS Bedrock