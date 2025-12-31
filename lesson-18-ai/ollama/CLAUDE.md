# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an Ollama management and experimentation workspace for running local Large Language Models (LLMs). The directory structure is organized around model management, GPU optimization, and web UI integration.

## Key Commands

### Model Management
```bash
# Pull specific models (configured set)
./ollama-pull.sh

# Update all existing models
./ollama-pull-all.sh

# List installed models (sorted)
./scripts/list_ollama.sh

# Advanced model management (pull/remove via Python)
cd scripts && python pull_ollama.py
```

### Service Management
```bash
# Check Ollama service status
sudo systemctl status ollama

# Restart Ollama service
sudo systemctl restart ollama

# View service logs
sudo journalctl -u ollama.service -n 50 --no-pager
```

### GPU Troubleshooting
```bash
# Check GPU status
nvidia-smi

# Fix GPU issues after suspend/resume
sudo ./gpu/fix-ollama-gpu.sh

# Run model with specific GPU settings
OLLAMA_NUM_GPU=50 OLLAMA_GPU_LIBRARY=/usr/lib/x86_64-linux-gnu/libcuda.so ollama run <model_name>
```

## Architecture

### Custom Configuration
- **Model Storage**: `/opt/ollama/.ollama/models` (non-standard location for disk space management)
- **Service Config**: SystemD service with custom environment variables for parallel serving
- **Performance**: `OLLAMA_NUM_PARALLEL=3 OLLAMA_MAX_LOADED_MODELS=2`

### Directory Structure
- **`/scripts/`**: Management utilities and Jupyter notebooks for analysis
- **`/custom-install/`**: Installation scripts with custom storage configuration
- **`/DeepSeek/`**: DeepSeek R1 model documentation (1.5B-14B variants)
- **`/Embed/`**: Embedding models (Snowflake Arctic, BGE-M3)
- **`/gpu/`**: GPU troubleshooting tools and SystemD service fixes
- **`/chat-ollama/`**: Web UI screenshots and RAG documentation

### Model Organization
Models are organized by provider/company in `ollama-pull.sh`:
- Google (Gemma), Meta (Llama), Microsoft (Phi)
- Chinese providers (DeepSeek, Qwen, Baichuan)
- Specialized models (code, math, medical, embeddings)

## Hardware Constraints

### GPU Limitations
- **Target Hardware**: RTX 4060 with 8GB VRAM
- **Issue**: GPU reinitialization required after Linux suspend/resume
- **Solution**: Manual NVIDIA module reload via scripts in `/gpu/`

### Storage Management
- Large models (up to 9+ GB each) stored in custom location
- Disk space monitoring essential for model collections
- Selective installation based on use case

## Web UI Integration

### Supported Interfaces
- **Open-WebUI**: Docker container on `http://localhost:3000/`
- **Chat-Ollama**: NextJS-based with RAG capabilities
- **ChromaDB**: Vector database for embeddings

### RAG Setup
- ChromaDB integration for document retrieval
- Embedding models: BGE-M3, Snowflake Arctic variants
- Knowledge base management through web interfaces

## Common Issues

### Ollama Upgrade Issues
- **Problem**: After upgrading ollama, service fails with permission denied errors
- **Root Cause**: Upgrade resets systemd service configuration, removing custom `OLLAMA_MODELS` environment variable
- **Solution**: Copy fixed service file with proper user and environment variables:
  ```bash
  sudo cp /home/papagame/projects/wgong/py4kids/lesson-18-ai/ollama/ollama.service.fixed2 /etc/systemd/system/ollama.service
  sudo systemctl daemon-reload && sudo systemctl restart ollama
  ```
- **Key Fix**: Service must run as `papagame` user (not `ollama`) to access models in `/home/papagame/.ollama/models/`

### GPU Problems
- CUDA library path issues after system suspend
- VRAM exhaustion requiring CPU fallback
- Driver module reloading needed post-hibernation

### Model Management
- Large download sizes requiring stable internet
- Version conflicts between model variants
- Storage space exhaustion from model accumulation

## Development Workflow

1. **Model Testing**: Use `ollama-pull.sh` to install curated model set
2. **Service Verification**: Check SystemD service status after changes
3. **GPU Validation**: Run `nvidia-smi` and test model inference
4. **Web UI Testing**: Verify integration with Open-WebUI or Chat-Ollama
5. **Performance Monitoring**: Check VRAM usage and parallel serving capacity