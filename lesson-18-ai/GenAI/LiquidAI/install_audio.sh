# requires python 3.12
# conda create -n liquid12 python=3.12
# conda activate liquid12

pip install liquid-audio
pip install "liquid-audio[demo]"
# Optional: faster attention on some GPUs
pip install flash-attn --no-build-isolation