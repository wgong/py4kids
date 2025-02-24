

## Open-WebUI

https://github.com/open-webui/open-webui

- 2025-02-23

```
conda create -n ollama python=3.11
conda activate ollama

pip install ollama  --upgrade       # v0.4.7
pip install open-webui  --upgrade   # v0.5.16

open-webui serve  
# v0.5.7 - building the best open-source AI user interface.

# access UI at http://localhost:8080

# monitor nvidia GPU usage
nvidia-smi
```