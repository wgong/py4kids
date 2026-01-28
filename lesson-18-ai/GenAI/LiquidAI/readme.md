## LFM2.5-1.2B-Instruct
- https://medium.com/data-science-in-your-pocket/tiny-model-real-power-a-handson-guide-to-lfm2-5-on-hugging-face-e7be0a9ab7d0



```bash
conda create -n liquidai python=3.11
conda activate liquidai

# Core libraries
pip install "transformers>=4.46.0" accelerate

# Optional but helpful: 4-bit / 8-bit loading to save memory
pip install bitsandbytes

```