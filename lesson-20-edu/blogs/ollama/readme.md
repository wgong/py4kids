
## store Model files in another location

see 
- https://claude.ai/chat/65cd7dca-e2a2-4417-ae5b-30ce2e4c3004
- https://claude.ai/project/cbc69e1a-e5bc-4cc4-a77b-f94cf268b3a6


run the following to install/upgrade Ollama
```
curl -fsSL https://ollama.com/install.sh | sh
```
The default OLLAMA_HOME=/usr/share/ollama

Update ollama service script
```
sudo nano /etc/systemd/system/ollama.service
```
by setting `ExecStart` as 
```
ExecStart=/bin/bash -c 'env > /tmp/ollama_env.log && OLLAMA_HOME=/usr/share/ollama OLLAMA_MODELS=/opt/ollama/.ollama/models /usr/local/bin/ollama serve'
User=root
Group=root
```

where OLLAMA_MODELS=/opt/ollama/.ollama/models
points to a location with sufficient space to store models

Execute
```
sudo systemctl daemon-reload
sudo systemctl restart ollama
sudo systemctl status ollama
# sudo systemctl stop ollama
```

Check the full logs for more detailed error information:
```
sudo journalctl -u ollama.service -n 50 --no-pager
```

Change ownership and permission
```
sudo chown -R $USER:$USER /opt/ollama
sudo chmod -R 755 /opt/ollama

ls -lA /opt/ollama/.ollama
# drwxr-xr-x 4 root root 4096 Oct 15 23:26 models

$ ls -lA /opt/ollama/.ollama/models
drwxr-xr-x 2 papagame papagame 20480 Nov 15 22:42 blobs
drwxr-xr-x 3 papagame papagame  4096 Oct 15 23:29 manifests

```

