

using FastMCP's built-in development server instead:
```
(mcp) C:\Users\p2p2l\projects\wgong\py4kids\lesson-18-ai\Agents\MCP\gemini\fastmcp\windows>fastmcp dev mcp_server.py
Need to install the following packages:
@modelcontextprotocol/inspector@0.13.0
Ok to proceed? (y) y

Starting MCP inspector...
⚙️ Proxy server listening on port 6277
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
```

open URL = http://127.0.0.1:6274/


install wsl: gong/gong 
```
cd /mnt/c/Users/p2p2l/projects/wgong/py4kids/lesson-18-ai/Agents/MCP/gemini/fastmcp

sudo apt update && sudo apt upgrade -y
sudo apt install wget curl -y

cd ~

# Download Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install
bash Miniconda3-latest-Linux-x86_64.sh

# Reload shell
source ~/.bashrc

$ conda --version
conda 25.3.1

python --version
Python 3.13.2

conda create -n mcp
conda activate mcp


sudo apt install python3-uvicorn
```
