import yaml
import json
import subprocess
from pytube import YouTube
from pathlib import Path
from time import time

# read json_data
file_json = "youtube-data.json"
file_yaml = "youtube-data.yaml"

if Path(file_json).exists():
    with open(file_json) as f:
        json_data = json.loads(f.read())
else:
    json_data = {}

with open(file_yaml) as f:
    url_dict = yaml.load(f, Loader=yaml.FullLoader)

for url in url_dict["todo"]:
    yt = YouTube(url)
    try:
        json_data.update({url : yt.title})
    except:
        json_data.update({url : url})
        
    try:
        file_mp4 = f"{yt.title}.mp4"
        if Path(file_mp4).exists():
            print(f"{file_mp4} already exists, skip...")
        else:
            print(f"Downloading {file_mp4} ...")
            t1 = time()
            subprocess.run(["pytube", url])
            t2 = time()
            print(f"... completed in {(t2-t1):.2f} sec")

        if url not in url_dict["done"]:
            url_dict["done"].append(url)
    except Exception as e:
        print(f"[Error] str(e)")
        if url not in url_dict["error"]:
            url_dict["error"].append(url)

# write yaml
with open(file_yaml, "w") as f:
    url_dict["todo"] = None
    yaml.dump(url_dict, f)

# write json_data
with open(file_json, "w") as f:
    f.write(json.dumps(json_data))