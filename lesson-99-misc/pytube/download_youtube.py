import yaml
import json
import subprocess
from pytube import YouTube
from pathlib import Path
from time import time

FILE_JSON = "youtube-data.json"
FILE_YAML = "youtube-list.yaml"
FILE_LOG = "youtube.log"

def _get_url_dict(d, key="todo"):
    res = d.get(key, [])
    return res if res else []

def _log(msg, file="pytube.log", print_flag=True, encoding="utf-8"):
    msg = f"{msg}\n"
    with open(file,"a+", encoding=encoding) as f:
        f.write(msg)
    if print_flag:
        print(msg)


# read yaml data
with open(FILE_YAML) as f:
    url_dict = yaml.load(f, Loader=yaml.FullLoader)
    
list_todo = _get_url_dict(url_dict, key="todo")
if not list_todo:
    import sys
    sys.exit()

list_done = _get_url_dict(url_dict, key="done")
list_error = _get_url_dict(url_dict, key="error")

# read json_data
if Path(FILE_JSON).exists():
    with open(FILE_JSON) as f:
        json_data = json.loads(f.read())
else:
    json_data = {}
    
for url in list_todo:
    yt = YouTube(url)
    try:
        json_data.update({url : yt.title})
    except:
        json_data.update({url : url})
        
    try:
        file_mp4 = f"{yt.title}.mp4"
        if Path(file_mp4).exists():
            _log(f"{file_mp4} already exists, skip...")
        else:
            _log(f"Downloading {file_mp4} ...")
            t1 = time()
            subprocess.run(["pytube", url])
            t2 = time()
            _log(f"... completed in {(t2-t1):.2f} sec")

        if url not in list_done:
            list_done.append(url)
    except Exception as e:
        _log(f"[Error] {str(e)}")
        if url not in list_error:
            list_error.append(url)

# write json_data
with open(FILE_JSON, "w") as f:
    f.write(json.dumps(json_data))
    
# write yaml
with open(FILE_YAML, "w") as f:
    url_dict.update({
            "todo": None,
            "done": list_done if list_done else None,
            "error": list_error if list_error else None
        })
    yaml.dump(url_dict, f)