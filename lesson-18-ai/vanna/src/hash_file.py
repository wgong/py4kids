"""
Download
```sh 
wget https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz

```

update 
ONNXMiniLM_L6_V2._MODEL_SHA256
in file ~/vanna/lib/python3.11/site-packages/chromadb/utils/embedding_functions.py

"""

# calculate hash
import hashlib
sha256_hash = hashlib.sha256()
fname = "onnx.tar.gz"

with open(fname, "rb") as f:
	# Read and update hash in chunks to avoid using too much memory
	for byte_block in iter(lambda: f.read(4096), b""):
		sha256_hash.update(byte_block)

print(sha256_hash.hexdigest())
# 913d7300ceae3b2dbc2c50d1de4baacab4be7b9380491c27fab7418616a16ec3