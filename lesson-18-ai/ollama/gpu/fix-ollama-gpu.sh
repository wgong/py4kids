#!/bin/bash
## /usr/local/bin/fix-ollama-gpu.sh

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
