# GPU is not loaded

common issues:
- If you don’t have enough VRAM it will use CPU.
- after ollama falls sleep, it won't load model into GPU

- https://github.com/ollama/ollama/issues/5464
Ollama fails to work with CUDA after Linux suspend/resume, unlike other CUDA services #5464


- https://forums.developer.nvidia.com/t/solution-for-nvidia-sleep-wake-issue-in-linux/110911


- https://www.reddit.com/r/LocalLLaMA/comments/1hqm2z6/ollama_not_using_gpu_need_help/  (no use)

    - This may only be an issue in Linux, but for me, CUDA in general only works after a fresh start and never works after it wakes up from from sleep mode

- https://www.reddit.com/r/ollama/comments/1c8ddv8/ollama_doesnt_use_gpu_pls_help/  (no use)

```
GPU has 8188MiB
qwen2.5:latest  4.7 GB
```

## reboot Linux as a workaround
```
OLLAMA_NUM_GPU=50 OLLAMA_GPU_LIBRARY=/usr/lib/x86_64-linux-gnu/libcuda.so ollama run qwen2.5

>>> what is 5!
very quick response

nvidia-smi
show GPU mem usuage
5740MiB /   8188MiB

see "gpu/gpu-rtx-4060-2024-09-28 21-26-31.png"
where "cuda_v12/ollama_llama_server       5238MiB"
shows  under "Processes" section
```

## Gemini

```
ls /usr/lib/x86_64-linux-gnu/libcuda.so
export OLLAMA_GPU_LIBRARY=/usr/lib/x86_64-linux-gnu/libcuda.so

echo $OLLAMA_NUM_GPU  # not set
export OLLAMA_NUM_GPU=50

OLLAMA_NUM_GPU=50 OLLAMA_GPU_LIBRARY=/usr/lib/x86_64-linux-gnu/libcuda.so ollama run qwen2.5

nvidia-smi  # check if model is loaded in GPU

# restart ollama
sudo systemctl status ollama
export CUDA_VISIBLE_DEVICES=0
sudo systemctl restart ollama
```

### linux - how to load GPU kernel after sleep

Identify the module name:
```
$ lsmod | grep nvidia
nvidia_uvm           4956160  2
nvidia_drm            122880  11
nvidia_modeset       1355776  13 nvidia_drm
nvidia              54386688  203 nvidia_uvm,nvidia_modeset
video                  73728  1 nvidia_modeset
```

Manually reload after sleep:
```
sudo modprobe nvidia
```

#### Ask Gemini

- https://gemini.google.com/app/743f567974638c56

1) Create a Script: Create a simple script that unloads and then reloads these modules.
NVIDIA Example (~/reload_nvidia.sh):

```
#!/bin/bash
sudo modprobe -r nvidia_uvm
sudo modprobe -r nvidia_modeset  # If it exists and is loaded
sudo modprobe -r nvidia
sudo modprobe nvidia
sudo modprobe nvidia_modeset
sudo modprobe nvidia_uvm
```

Make it Executable: `chmod a+x reload_nvidia.sh`


2) Systemd Service (for Automation)

Create a Service File: This service will run the script from step 1 automatically after suspend.
NVIDIA Example: Create a file at /etc/systemd/system/resume-nvidia.service:

```
[Unit]
Description=Reload NVIDIA Modules After Suspend
After=suspend.target sleep.target

[Service]
Type=oneshot
ExecStart=~/reload_nvidia.sh

[Install]
WantedBy=suspend.target sleep.target

```

3) Enable and Start the Service:

```
sudo systemctl daemon-reload
sudo systemctl enable resume-nvidia.service  # Or resume-amdgpu.service
```