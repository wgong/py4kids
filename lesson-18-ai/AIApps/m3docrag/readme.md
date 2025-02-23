
local dir: ~/projects/wgong/m3docrag

cloned: https://github.com/wgong/m3docrag


### Setup

```
conda create -n m3doc python=3.11
conda activate m3doc

cd ~/projects/wgong
git clone https://github.com/bloomberg/m3docrag.git

# clear cache
pip cache purge
rm -rf /tmp/pip-*  # Clear temp pip files
rm -rf build/ dist/ *.egg-info/  # Clear local build files

# install torch
pip install torch>=2.0.0

pip install -e . --verbose

pip install pdf2image
pip install poppler-utils


cd /opt
sudo mkdir m3doc
sudo chown -R papagame:papagame /opt/m3doc/

export LOCAL_ROOT="/opt/m3doc"    # custom folder
export LOCAL_DATA_DIR="$LOCAL_ROOT/job/datasets"
export LOCAL_EMBEDDINGS_DIR="$LOCAL_ROOT/job/embeddings"
export LOCAL_MODEL_DIR="$LOCAL_ROOT/job/model"
export LOCAL_OUTPUT_DIR="$LOCAL_ROOT/job/output"


# Download pdf dataset
# see https://github.com/bloomberg/m3docrag/blob/main/m3docvqa/README.md
cd /home/papagame/projects/wgong/m3docrag/m3docvqa
pip install -e .

playwright install
playwright install-deps

pytest tests


# clone Models
cd $MY_LOCAL_MODEL_DIR

git clone https://huggingface.co/vidore/colpaligemma-3b-pt-448-base # ColPali backbone
git clone https://huggingface.co/vidore/colpali-v1.2 # ColPali adapter
git clone https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct # VQA

HuggingFace models:
- colpali-v1.2: https://huggingface.co/vidore/colpali-v1.2
- vidore/colpaligemma-3b-mix-448-base: https://huggingface.co/vidore/colpaligemma-3b-mix-448-base
- Qwen/Qwen2-VL-7B-Instruct: https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct

# download PDF files

https://github.com/allenai/multimodalqa

cd /opt/m3doc/job/datasets

git clone https://github.com/allenai/multimodalqa.git

```


### Playwright

Playwright is a modern automation testing framework developed by Microsoft that allows you to automate web browsers (Chromium, Firefox, and WebKit). It's particularly useful for:

Browser Testing


End-to-end testing
Cross-browser testing
UI testing
Web scraping
Test automation

Key features:

Supports multiple programming languages (Python, JavaScript, Java, .NET)
Auto-wait capabilities
Network interception
Mobile device emulation
Screenshots and video recording
PDF generation