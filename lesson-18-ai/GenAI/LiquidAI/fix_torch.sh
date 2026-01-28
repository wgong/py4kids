# Reinstall PyTorch with proper CUDA 11.7 support for sm_61:
# see ~/projects/Proj-Geometry-of-Meaning/semanscope/archive/docs/Torch-GPU.md
pip uninstall torch torchvision torchaudio
pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121 --index-url https://download.pytorch.org/whl/cu121