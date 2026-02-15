# Setup ubuntu=wengong

```bash

# ollama
sudo snap install curl
curl -fsSL https://ollama.com/install.sh | sh

ollama pull 
qwen3-vl:8b
qwen3:4b
qwen3-embedding:0.6b
qwen3-embedding:4b
qwen2.5
qwen2.5-coder:7b

ollama pull embeddinggemma:latest
ollama pull phi4:latest 
ollama pull gemma3:latest
ollama pull gemma3:12b
ollama pull lfm2.5-thinking
ollama pull deepseek-ocr
ollama pull phi4-mini
ollama pull nomic-embed-text-v2-moe:latest
ollama pull translategemma:latest
ollama pull translategemma:12b
ollama pull qwen3-vl:4b

# git
ssh-keygen -t ed25519 -C "wen.gong@gmail.com"
# ~/.ssh/id_ed25519.pub
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

git config --global user.email "wen.gong@gmail.com"
git config --global user.name "Gong"


conda create -n zinets python=3.11
conda create -n st python=3.11

# repos
git clone git@github.com:wgong/py4kids.git
git clone git@github.com:wgong/DeepCode.git
git clone git@github.com:digital-duck/zinets_radicals.git
git clone git@github.com:digital-duck/st_semantics.git
git clone git@github.com:digital-duck/maniscope.git
git clone git@github.com:digital-duck/semanscope.git
git clone git@github.com:digital-duck/phate-manifold-metrics.git
git clone git@github.com:digital-duck/oracle.git
git clone git@github.com:digital-duck/orascope.git
git clone git@github.com:digital-duck/SPL.git
git clone git@github.com:digital-duck/SPL-flow.git
git clone git@github.com:digital-duck/zinets.git

# npm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
command -v nvm
nvm install --lts
npm --version
11.8.0
node --version
v24.13.1

# claude
npm install -g @anthropic-ai/claude-code
claude --version
2.1.42 (Claude Code)


# gemini 
npm install -g @google/gemini-cli
gemini --version
0.28.2




# nvidia-smi
ubuntu-drivers devices
sudo ubuntu-drivers autoinstall
sudo apt update
sudo apt install nvidia-driver-535
sudo reboot

# screenshot 
sudo apt install flameshot
```
