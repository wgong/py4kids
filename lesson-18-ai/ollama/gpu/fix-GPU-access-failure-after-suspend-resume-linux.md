# Ollama: Fixing GPU Access Failure After Suspend/Resume on Linux

If you're using Ollama to run local LLMs on Linux and have encountered the frustrating issue where your GPU becomes inaccessible after your system wakes up from suspend or hibernate, you're not alone. This seems to be a known problem affecting both NVIDIA and AMD GPUs on various Linux distributions. 

## The Problem

After suspending your Linux system and later resuming it, Ollama may fail to utilize your GPU for inference.  You might still be able to run models, but they'll likely be using your CPU, leading to significantly slower performance. Restarting the Ollama service doesn't resolve the issue; only a full system reboot seems to fix it.

This problem has been reported on the [Ollama GitHub issue tracker](https://github.com/ollama/ollama/issues/5464) by multiple users, running different hardware and software configurations, including:

*   **GPUs:** NVIDIA (e.g., RTX 3070, RTX 3090), AMD
*   **Operating Systems:** Ubuntu, Fedora, Arch Linux, macOS, and others
*   **Kernel Versions:** Various versions

## The Root Cause (As Far As We Know)

The exact root cause is still under investigation by the Ollama developers. However, based on user reports and troubleshooting, it appears to be related to how the GPU driver modules, particularly the `nvidia_uvm` module on NVIDIA systems, are handled during the suspend/resume process. It seems these modules don't always get properly unloaded or reinitialized after waking the system, leading to Ollama being unable to access the GPU.

## The Workaround: Reloading the GPU Driver Module

Thanks to the combined efforts of the "Ask Ubuntu" community (https://askubuntu.com/questions/1228423/how-do-i-fix-cuda-breaking-after-suspend/1503961#1503961), a reliable workaround has been found. It involves stopping the Ollama service, reloading the problematic `nvidia_uvm` kernel module, and then restarting Ollama.

Here's how to implement it:

### 1. Create a Script

Create a script file (e.g., `/usr/local/bin/fix-ollama-gpu.sh`) with the following contents:

```bash
#!/bin/bash

echo "Stopping ollama"
if ! systemctl stop ollama; then
    echo "Error: Failed to stop Ollama service"
    exit 1
fi

echo "Calling daemon reload"
if ! systemctl daemon-reload; then
    echo "Error: Failed to reload systemd daemon"
    exit 1
fi

echo "Removing nvidia_uvm"
if ! rmmod nvidia_uvm; then
    echo "Error: Failed to remove nvidia_uvm module"
    exit 1
fi

echo "Loading nvidia_uvm"
if ! modprobe nvidia_uvm; then
    echo "Error: Failed to load nvidia_uvm module"
    exit 1
fi

echo "Starting ollama again"
if ! systemctl start ollama; then
    echo "Error: Failed to start Ollama service"
    exit 1
fi

echo "Ollama GPU fix applied successfully"
exit 0
```

***Note for AMD Users***: If you have an AMD GPU, you'll need to modify the script to target the `amdgpu` module instead of `nvidia_uvm`. Replace `rmmod nvidia_uvm` with `rmmod amdgpu` and `modprobe nvidia_uvm` with `modprobe amdgpu`.

### 2. Make the Script Executable

```bash
sudo chmod a+x /usr/local/bin/fix-ollama-gpu.sh
```

### 3. Run the Script After Resume (Manually)

After your system wakes up from suspend, open a terminal and run the script with sudo privileges:

```bash
sudo /usr/local/bin/fix-ollama-gpu.sh
```

### 4. Automate with systemd (Optional but Recommended)

To avoid running the script manually every time, you can create a systemd service that automatically executes it after suspend/resume:

#### Create a service file:

```bash
sudo nano /etc/systemd/system/fix-ollama-gpu.service
```

#### Paste the following into the service file:

```
[Unit]
Description=Fix Ollama GPU access after suspend
After=sleep.target suspend.target hibernate.target hybrid-sleep.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/fix-ollama-gpu.sh

[Install]
WantedBy=sleep.target suspend.target hibernate.target hybrid-sleep.target
```

***Important***: Make sure the `ExecStart` path matches where you saved your script.

#### Enable and start the service:


```bash
sudo systemctl daemon-reload
sudo systemctl enable fix-ollama-gpu.service
sudo systemctl restart ollama
```

Now, the script should run automatically whenever your system resumes from sleep, fixing the GPU access issue for Ollama.


#### 

### Important Notes
- Root Privileges: This script requires root privileges because it interacts with kernel modules and systemd.
- Error Handling: The script includes basic error handling to make it more robust.
- AMD Adaptation: Remember to adjust the script for AMD GPUs by replacing nvidia_uvm with amdgpu.
- Temporary Workaround: This is a workaround, not a permanent fix. The Ollama developers are aware of the issue and are hopefully working on a proper solution.