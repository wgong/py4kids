# Configuring Ollama with Custom Model Storage Location

This guide explains how to set up Ollama to store model files in a custom location, which is particularly useful when you need more storage space than available in the default location.

## Default Configuration
- Default `OLLAMA_HOME`: `/usr/share/ollama`
- Default model storage location: Within `OLLAMA_HOME`

## Installation/Upgrade

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Configuration Steps

### 1. Update Ollama Service Configuration

Edit the systemd service file:
```bash
sudo nano /etc/systemd/system/ollama.service
```

Add or modify these lines:
```ini
[Service]
ExecStart=/bin/bash -c 'env > /tmp/ollama_env.log && OLLAMA_HOME=/usr/share/ollama OLLAMA_MODELS=/opt/ollama/.ollama/models /usr/local/bin/ollama serve'
User=root
Group=root
```

### 2. Create and Configure Custom Model Directory

```bash
# Set up permissions for custom model directory
sudo chown -R $USER:$USER /opt/ollama
sudo chmod -R 755 /opt/ollama
```

### 3. Restart Ollama Service

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
sudo systemctl status ollama
```

### 4. Verify Configuration

Check service status and logs:
```bash
# View recent logs
sudo journalctl -u ollama.service -n 50 --no-pager

# Verify directory permissions
ls -lA /opt/ollama/.ollama
ls -lA /opt/ollama/.ollama/models
ls -lA /usr/share/ollama
```

Expected directory structure:
```
/opt/ollama/.ollama/models/
├── blobs/
└── manifests/

/usr/share/ollama/
└── .ollama/
```

### 5. Verify Service

Visit `http://127.0.0.1:11434` in your browser. You should see:
```
Ollama is running
```

## Troubleshooting

- If the service fails to start, check the logs using `journalctl`
- Ensure all directories have correct ownership and permissions
- Verify that the custom storage location has sufficient disk space
- Make sure both `OLLAMA_HOME` and `OLLAMA_MODELS` paths exist and are accessible

## Important Notes

- The `OLLAMA_MODELS` path (`/opt/ollama/.ollama/models`) should point to a location with sufficient storage space for your models
- The service must run as root to ensure proper access to system resources
- Environment variables are logged to `/tmp/ollama_env.log` for debugging purposes