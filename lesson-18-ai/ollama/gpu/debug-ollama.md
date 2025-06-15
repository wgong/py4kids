## check ollama service 
```bash
sudo systemctl status ollama

● ollama.service - Ollama Service
     Loaded: loaded (/etc/systemd/system/ollama.service; enabled; vendor preset: enabled)
     Active: activating (auto-restart) (Result: exit-code) since Sat 2025-05-31 16:33:01 EDT; 2s ago
    Process: 7293 ExecStart=/usr/local/bin/ollama serve (code=exited, status=1/FAILURE)
   Main PID: 7293 (code=exited, status=1/FAILURE)
        CPU: 11ms

```

## check ollama log

```
journalctl -u ollama --no-pager

cat ~/.ollama/logs/server.log
```

## run ollama manually

```
ollama serve

time=2025-05-31T16:43:14.174-04:00 level=INFO source=routes.go:1205 msg="server config" env="map[CUDA_VISIBLE_DEVICES: GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_CONTEXT_LENGTH:4096 OLLAMA_DEBUG:INFO OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://127.0.0.1:11434 OLLAMA_INTEL_GPU:false OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:/home/papagame/.ollama/models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NEW_ENGINE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NUM_PARALLEL:0 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_SCHED_SPREAD:false ROCR_VISIBLE_DEVICES: http_proxy: https_proxy: no_proxy:]"
time=2025-05-31T16:43:14.313-04:00 level=INFO source=images.go:463 msg="total blobs: 132"
time=2025-05-31T16:43:14.318-04:00 level=INFO source=images.go:470 msg="total unused blobs removed: 0"
time=2025-05-31T16:43:14.321-04:00 level=INFO source=routes.go:1258 msg="Listening on 127.0.0.1:11434 (version 0.7.1)"
time=2025-05-31T16:43:14.323-04:00 level=INFO source=gpu.go:217 msg="looking for compatible GPUs"
time=2025-05-31T16:43:14.474-04:00 level=INFO source=types.go:130 msg="inference compute" id=GPU-7e54064f-5498-250d-d6f5-696ed48dca43 library=cuda variant=v12 compute=6.1 driver=12.4 name="NVIDIA GeForce GTX 1080 Ti" total="10.9 GiB" available="10.3 GiB"
[GIN] 2025/05/31 - 16:43:30 | 200 |    6.716153ms |       127.0.0.1 | HEAD     "/"
[GIN] 2025/05/31 - 16:43:30 | 200 |  145.162462ms |       127.0.0.1 | GET      "/api/tags"

```


# Focused Troubleshooting Steps

That's excellent news that you can start Ollama manually and use a GPU-loaded model like Qwen2.5! This significantly narrows down the potential causes of the problem.

Since Ollama works manually, the issue is almost certainly related to how the **systemd service** is configured or the **environment** it runs in. The core Ollama application and your GPU setup are fine.

Here's a focused troubleshooting guide, knowing it works manually:

## The Problem: Systemd Service Environment vs. Manual Environment

When you run `ollama serve` manually, it inherits your user's environment variables, shell settings, and potentially other paths. When `systemd` starts the service, it runs in a more isolated and often minimal environment.

This isolation is usually the culprit.

## Focused Troubleshooting Steps

1.  **Re-check `ollama.service` Status and Logs (Crucial First Step):**
    Even though you know it works manually, the error messages in the service logs will be the most direct clue.
    ```bash
    sudo systemctl status ollama
    journalctl -xeu ollama --no-pager
    ```
    Pay close attention to any "Failed," "Error," or "Permission denied" messages. Look for lines indicating issues *before* Ollama even tries to load models.

2.  **User and Permissions Mismatch:**
    * **Identify the service user:** Open the `ollama.service` file (or its override):
        ```bash
        sudo systemctl edit --full ollama.service
        # or if you created an override:
        sudo systemctl edit ollama.service
        ```
        Look for the `User=` and `Group=` lines under the `[Service]` section. It's often `ollama` or `root` by default, but it could be your username if you modified it.
    * **Verify ownership of Ollama directories:** Ensure the user specified in `User=` has ownership of the Ollama home directory and the models directory.
        * Typically `~/.ollama` (which for the `ollama` user would be `/home/ollama/.ollama`).
        * And `~/.ollama/models`.
        * **Example (if service user is `ollama`):**
            ```bash
            sudo chown -R ollama:ollama /home/ollama/.ollama
            # If Ollama is installed to use your user's home directory
            # but the service runs as 'ollama' user:
            # You might need to adjust OLLAMA_HOME or OLLAMA_MODELS in the service file.
            ```
        * **Example (if service user is *your* username, e.g., `youruser`):**
            ```bash
            sudo chown -R $USER:$USER ~/.ollama
            ```
    * **Group Memberships (especially for GPU):** The service user (e.g., `ollama` or whatever is specified) needs to be in the `video` and `render` groups to access the GPU.
        ```bash
        sudo usermod -aG video <service_user>
        sudo usermod -aG render <service_user>
        ```
        Replace `<service_user>` with the actual user defined in your `ollama.service` file (e.g., `ollama`).
        **Crucially:** After adding a user to groups, you need to **reboot the system** for the group changes to take full effect on services.

3.  **Environment Variables in Systemd:**
    This is a very common reason for manual success but service failure. When you run `ollama serve` manually, environment variables like `OLLAMA_MODELS`, `OLLAMA_HOST`, `LD_LIBRARY_PATH` (for GPU drivers), etc., are usually set. Systemd doesn't automatically inherit these.

    * **`OLLAMA_MODELS`:** If your models are not in the default location for the service user, you *must* explicitly set `OLLAMA_MODELS` in the service file.
        ```bash
        sudo systemctl edit ollama.service
        ```
        Add (or modify) under `[Service]`:
        ```
        [Service]
        Environment="OLLAMA_MODELS=/path/to/your/models"
        ```
        (Replace `/path/to/your/models` with the *absolute* path where your models are located, e.g., `/home/youruser/.ollama/models`).

    * **`OLLAMA_HOST` (less likely, but check if you customized):** If you've manually set `OLLAMA_HOST` (e.g., to a specific IP or port), ensure it's also set in the service file if you want the service to use it.

    * **GPU Driver Paths (`LD_LIBRARY_PATH`):** While `systemd` is usually good at handling standard library paths, sometimes specific GPU driver installations or non-standard `LD_LIBRARY_PATH` settings are needed. If your `journalctl` output mentions "cannot open shared object file" or similar library errors related to CUDA/ROC, you might need to set `LD_LIBRARY_PATH`.
        ```bash
        sudo systemctl edit ollama.service
        ```
        Add under `[Service]`:
        ```
        [Service]
        Environment="LD_LIBRARY_PATH=/path/to/your/cuda/lib64:/path/to/other/libs"
        ```
        (Find the correct paths from your manual setup if needed).

    * **After any `systemctl edit` changes:**
        ```bash
        sudo systemctl daemon-reload
        sudo systemctl restart ollama
        journalctl -xeu ollama --no-pager # Check logs immediately!
        ```

4.  **SELinux or AppArmor (Less Common, but Possible):**
    If you have SELinux or AppArmor enabled and they are configured restrictively, they might be preventing the `ollama.service` from accessing necessary files or network ports.
    * **Check SELinux status:** `sestatus`
    * **Check AppArmor status:** `sudo apparmor_status`
    * If they are enforcing, temporarily disabling them (for testing purposes only, not recommended long-term) or checking their logs for denials might reveal the issue. For AppArmor, check `/var/log/syslog` or `dmesg` for "DENIED" messages related to Ollama.

5.  **Corrupted Systemd Unit File:**
    If you've heavily modified the `ollama.service` file and it's now broken, you might consider letting the official install script regenerate it.
    ```bash
    # Backup existing service file if you made custom changes
    # sudo cp /etc/systemd/system/ollama.service /etc/systemd/system/ollama.service.bak

    # Re-run the installer
    curl -fsSL https://ollama.com/install.sh | sh

    # Check the new service file and adjust OLLAMA_MODELS if necessary
    sudo systemctl edit ollama.service
    sudo systemctl daemon-reload
    sudo systemctl restart ollama
    ```

**In summary, since manual startup works, the focus is almost entirely on the `ollama.service` unit file:**

* **User/Permissions:** Does the user running the service have access to everything Ollama needs? (Especially `~/.ollama` and GPU access).
* **Environment Variables:** Are all necessary environment variables (like `OLLAMA_MODELS` and potentially `LD_LIBRARY_PATH`) correctly set within the service definition?

Go through these steps methodically, checking the `journalctl` logs after each change. You're very close to getting this resolved!


## FIX

```
sudo chown -R ollama:ollama /home/papagame/.ollama

# sudo nano /etc/systemd/system/ollama.service
# change user/group from ollama to papagame
sudo systemctl edit ollama.service

sudo usermod -aG video papagame  # ollama
sudo usermod -aG render papagame  # ollama


sudo systemctl daemon-reload
sudo systemctl enable fix-ollama-gpu.service
sudo systemctl start|status|stop|restart ollama
```

recent ollama install uses OLLAMA_MODELS=~/.ollama/models


see `py4kids/lesson-18-ai/ollama/gpu/fix-GPU-access-failure-after-suspend-resume-linux.md` for fixing GPU reload after Ubuntu suspend
