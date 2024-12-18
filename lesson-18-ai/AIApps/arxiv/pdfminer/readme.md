https://claude.ai/chat/115fdf3d-a30b-43a6-9342-99ea1872d6a3


```
conda create -n arxiv python=3.11
conda activate arxiv

pip install -r requirements.txt

cd pdfminer
python process_pdf ../data/llmspec.pdf -v
```