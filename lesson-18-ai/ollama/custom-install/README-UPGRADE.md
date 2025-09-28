# Ollama Upgrade Fix Guide

## Overview

This guide provides step-by-step instructions to fix Ollama service issues that occur after upgrading. The primary issue is that Ollama upgrades reset the systemd service configuration, causing permission errors and service failures.

## When to Use This Guide

Use this guide when you encounter any of these symptoms after an Ollama upgrade:

- Service stuck in restart loop with permission denied errors
- Error: `open /usr/share/ollama/.ollama/id_ed25519: permission denied`
- `ollama list` shows "could not connect to a running Ollama instance"
- Manual `ollama serve` works but systemd service fails

## Quick Fix (5 Steps)

### Step 1: Stop any running processes
```bash
# Kill any existing ollama processes to avoid port conflicts
pkill -f ollama
```

### Step 2: Apply the fixed service configuration
```bash
sudo cp -f /home/papagame/projects/wgong/py4kids/lesson-18-ai/ollama/ollama.service.fixed2 /etc/systemd/system/ollama.service
```

### Step 3: Reload and restart service
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

### Step 4: Verify service is running
```bash
sudo systemctl status ollama
```

**Expected output:**
```
● ollama.service - Ollama Service
     Loaded: loaded (/etc/systemd/system/ollama.service; enabled; vendor preset: enabled)
     Active: active (running) since [timestamp]
   Main PID: [number] ((ollama))
      Tasks: 1 (limit: 57615)
     Memory: [size]
        CPU: [time]
     CGroup: /system.slice/ollama.service
             └─[number] "[(ollama)]"
```

### Step 5: Test functionality
```bash
ollama list
ollama run gemma3 "What is 2+2?"
```

## Troubleshooting

### If service still fails to start:

1. **Check logs for specific errors:**
   ```bash
   sudo journalctl -u ollama.service -n 20 --no-pager
   ```

2. **Verify models location:**
   ```bash
   ls ~/.ollama/models/manifests/registry.ollama.ai/library/
   ```

3. **Test manual startup:**
   ```bash
   ollama serve
   ```
   If manual startup works but service doesn't, the issue is with service configuration.

### Common Issues:

- **Port already in use**: Make sure to kill existing ollama processes with `pkill -f ollama`
- **Permission denied**: Ensure the service runs as `papagame` user (not `ollama`)
- **Models not found**: Verify `OLLAMA_MODELS=/home/papagame/.ollama/models` is set in service file

## Prevention for Future Upgrades

**Always check these after upgrading Ollama:**

1. **Service configuration reset check:**
   ```bash
   cat /etc/systemd/system/ollama.service | grep OLLAMA_MODELS
   ```
   If this returns nothing, the configuration was reset.

2. **Quick prevention script:**
   ```bash
   # After any ollama upgrade, run:
   sudo cp -f /home/papagame/projects/wgong/py4kids/lesson-18-ai/ollama/ollama.service.fixed2 /etc/systemd/system/ollama.service
   sudo systemctl daemon-reload
   sudo systemctl restart ollama
   ```

## Key Technical Details

### What the fix does:
- Changes service user from `ollama` to `papagame` (who owns the models)
- Sets `OLLAMA_MODELS=/home/papagame/.ollama/models` environment variable
- Ensures proper PATH for CUDA and system binaries

### Why upgrades break the service:
- Ollama installer overwrites systemd service file
- Default configuration uses system locations that `ollama` user can't access
- Custom model location configuration is lost

## Success Verification Checklist

- [ ] `sudo systemctl status ollama` shows "active (running)"
- [ ] No permission errors in `sudo journalctl -u ollama.service -n 10`
- [ ] `ollama list` shows all your models
- [ ] Model inference works: `ollama run gemma3 "test"`
- [ ] GPU detected in logs: "NVIDIA GeForce GTX 1080 Ti"
- [ ] Service starts automatically after reboot

## Emergency Fallback

If the fix doesn't work, you can always run ollama manually while troubleshooting:

```bash
# Stop the service
sudo systemctl stop ollama

# Run manually (will work with your user environment)
ollama serve

# In another terminal, test:
ollama list
```

This allows you to continue using ollama while diagnosing service issues.