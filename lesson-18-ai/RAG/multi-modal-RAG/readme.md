Chinese Textbook project


## Multi-modal Retrieval
- [M3DOCRAG](https://arxiv.org/pdf/2411.04952): Multi-modal Retrieval is What You Need for Multi-page Multi-document Understanding (M3DocRAG with ColPali and Qwen2-VL 7B achieves superior performance than many strong baselines, including state-of-the-art performance in MP-DocVQA)
    - [code coming soon](https://m3docrag.github.io/)

- [ColPali](https://github.com/illuin-tech/colpali) - Efficient Document Retrieval with Vision Language Models
    - combining ColBERT and PaliGemma, to leverage VLMs to construct efficient multi-vector embeddings in the visual space for document retrieval
    - [Byaldi](https://github.com/AnswerDotAI/byaldi) is a new library by answer.ai to easily use ColPali

- [Qwen2-VL-7B](https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct)

- [ColPali Qwen2VL Demo code by Smol-Vision](https://github.com/merveenoyan/smol-vision/blob/main/ColPali_%2B_Qwen2_VL.ipynb) - Recipes for shrinking, optimizing, customizing cutting edge vision and multimodal AI models.


### setup 
```bash
# create virtual_env
conda create -n rag python=3.11
conda activate rag

# check cuda version
nvidia-smi   # 12.4

# install pytorch
## pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt

# install CUDA

# check Ubuntu version
lsb_release -a   # Ubuntu 22.04.5 LTS

# Add NVIDIA package repositories
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda-repo-ubuntu2204-12-1-local_12.1.0-530.30.02-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-1-local_12.1.0-530.30.02-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-1-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda

# pdf util for Linux
sudo apt-get install -y poppler-utils

pip install -r requirements.txt
```

## taxai

- https://github.com/wgong/txtai


## CLIP
combine text and image embedding
- https://g.co/gemini/share/e577a92ff2ee