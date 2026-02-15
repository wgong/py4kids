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
git@github.com:wgong/py4kids.git
git@github.com:wgong/DeepCode.git

git@github.com:digital-duck/zinets.git


# nvidia-smi
ubuntu-drivers devices
sudo ubuntu-drivers autoinstall
sudo apt update
sudo apt install nvidia-driver-535
sudo reboot

# screenshot 
sudo apt install flameshot
```
