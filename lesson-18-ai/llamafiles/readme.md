# llama.cpp / ggml.ai / llamafile

make open LLMs much more accessible to both developers and end users. We're doing that by combining llama.cpp with Cosmopolitan Libc into one framework that collapses all the complexity of LLMs down to a single-file executable (called a "llamafile") that runs locally on most computers, with no installation.

https://github.com/Mozilla-Ocho/llamafile


## Intro
GitHub: https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file

YouTube: https://youtu.be/-mRi-B3t6fA?si=GwTAzlsSxc7EX5-D


## Setup
./llamafile.exe --server --host 0.0.0.0 --port 9000 -m /opt/model/Meta-Llama-3-8B-Instruct.Q8_0.gguf


### Local
```
cd ~/Downloads/llamafile
./llava-v1.5-7b-q4.llamafile --help
./llava-v1.5-7b-q4.llamafile --port 9000 # open URL=localhost:9000

```

## API

create `test_llama_cpp.py`
```
#!/usr/bin/env python3
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:9000/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required"
)
completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "system", "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."},
        {"role": "user", "content": "Write a limerick about python exceptions"}
    ]
)
print(completion.choices[0].message)

```
in terminal
```
python test_llama_cpp.py
```


## Using llamafile with external weights

download zip from https://github.com/Mozilla-Ocho/llamafile/releases

see `~/Downloads/llamafile/llamafile-0.8.12-DIST`

## Issues

### Fail to start on Linux
- Problem:
    - https://github.com/Mozilla-Ocho/llamafile/issues/513

- Solution:
    - https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file#gotchas-and-troubleshooting

```
sudo wget -O /usr/bin/ape https://cosmo.zip/pub/cosmos/bin/ape-$(uname -m).elf
sudo chmod +x /usr/bin/ape
sudo sh -c "echo ':APE:M::MZqFpD::/usr/bin/ape:' >/proc/sys/fs/binfmt_misc/register"
sudo sh -c "echo ':APE-jart:M::jartsr::/usr/bin/ape:' >/proc/sys/fs/binfmt_misc/register"
```

It works great

### Creating a llamafile of a TTS Model #508
https://github.com/Mozilla-Ocho/llamafile/discussions/508

tortoise-tts (https://github.com/neonbjb/tortoise-tts)

