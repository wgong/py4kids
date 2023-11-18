"""
Instructions:
1) add YouTube URL(s) to "youtube-list.yaml" under 1_todo
2) $ python download_youtube.py
3) downloaded media files are saved to sub-folder: "media"
4) file "youtube-data.json" tracks downloaded files in the past


pip install unicodedata2  # to normalize unicode
"""

import yaml
import json
import subprocess
from pytube import YouTube
from pathlib import Path
from time import time
from datetime import datetime
import shutil
import string
# import re
# import unicodedata


FILE_JSON = "youtube-data.json"
FILE_YAML = "youtube-list.yaml"
FILE_LOG = "youtube.log"
TARGET = "media"

TAG_TODO = "1_todo"
TAG_ERROR = "2_error"
TAG_DONE = "3_done"
TAG_ARCHIVE = "4_archive"

target_path = Path(TARGET)
if not target_path.exists():
    target_path.mkdir(parents=True, exist_ok=True)

def _get_url_dict(d, key=TAG_TODO):
    res = d.get(key, [])
    return res if res else []

def _log(msg, file="pytube.log", print_flag=True, encoding="utf-8"):
    msg = f"{msg}\n"
    with open(file,"a+", encoding=encoding) as f:
        f.write(msg)
    if print_flag:
        print(msg)

def _parse_title(url):
    title = url.split("/")[-1]
    if "v=" in title:
        title = title.split("v=")[-1]
    return title



def remove_punctuation(text):
    """Removes punctuation from a Unicode string.

    Args:
        text: The Unicode string to remove punctuation from.

    Returns:
        A Unicode string with the punctuation removed.
    """
    table = str.maketrans('', '', string.punctuation.replace('.',''))
    return text.translate(table).strip()

# read yaml data
with open(FILE_YAML) as f:
    url_dict = yaml.load(f, Loader=yaml.FullLoader)
    
list_todo = _get_url_dict(url_dict, key=TAG_TODO)
if not list_todo:
    import sys
    sys.exit()

list_done = _get_url_dict(url_dict, key=TAG_DONE)
list_error = _get_url_dict(url_dict, key=TAG_ERROR)
list_archive = _get_url_dict(url_dict, key=TAG_ARCHIVE)

# read json_data
if Path(FILE_JSON).exists():
    with open(FILE_JSON, encoding="utf-8") as f:
        json_data = json.loads(f.read())
else:
    json_data = {}
    
for url in list_todo:
    # skip if url found in youtube-data.json

    if url in json_data:
        print(f"Skip: {url} already downloaded, title: '{json_data[url]}' ")
        continue

    # https://stackoverflow.com/questions/76129007/pytube-keyerror-streamdata-while-downloading-a-video
    # yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
    # fixed after upgrading pytube from 12.1.2 to 15.0.0
    yt = YouTube(url)
    try:
        yt_title = yt.title
    except:
        yt_title = _parse_title(url)
    json_data.update({url : str(yt_title)})
        
    file_mp4 = remove_punctuation(yt_title) + ".mp4"
    file_path = Path(file_mp4)
    if file_path.exists():
        _log(f"'{file_mp4}' already exists, skip ...")
    else:
        _log(f"Downloading '{file_mp4}' \n\t from url = {url} ...")
        t1 = time()
        p = subprocess.run(["pytube", url], stderr=subprocess.PIPE)
        t2 = time()
        if p.stderr:
            err = p.stderr.decode("utf-8")
            _log(f"[Error] {err}")
            if url not in list_error:
                err_msg = f"{url} == {err}"
                list_error.append(err_msg)
            continue

        if file_path.exists():
            shutil.move(file_path, target_path/file_path)

            if url not in list_done:
                list_done.append(url)
            _log(f"...... completed in {(t2-t1):.2f} sec")
        else:
            _log(f"[ERROR] failed to download {url}")

# write json_data
# https://stackoverflow.com/questions/18337407/saving-utf-8-texts-with-json-dumps-as-utf-8-not-as-a-u-escape-sequence

with open(FILE_JSON, "w", encoding="utf-8") as f:
    f.write(json.dumps(json_data, ensure_ascii=False))
    
# backup FILE_YAML 
ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
shutil.copyfile(FILE_YAML, Path("log") / f"{FILE_YAML}.{ts}")
## 2nd option
# shutil.copy(src, dst)   # dst can be a folder


# write yaml
with open(FILE_YAML, "w") as f:
    url_dict.update({
            TAG_TODO: None,
            TAG_ERROR: list_error if list_error else None,
            TAG_DONE: list_done if list_done else None,
            TAG_ARCHIVE: list_archive if list_archive else None,
        })
    yaml.dump(url_dict, f)