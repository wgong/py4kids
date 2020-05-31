import json
import logging
import os, glob
from pathlib import Path
from urllib.request import urlopen, Request

TYPES = {'image/jpeg', 'image/png'}

def get_logger(logger_name):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(logger_name)

logger = get_logger(__name__)


def rm_thumbnail(image_folder="images"):
    for f in glob.glob(f"{image_folder}/*_thumbnail.*"):
        os.remove(f)

def get_links(client_id):
    headers = {'Authorization': 'Client-ID {}'.format(client_id)}
    req = Request('https://api.imgur.com/3/gallery/random/random/', headers=headers, method='GET')
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    return [item['link'] for item in data['data'] if 'type' in item and item['type'] in TYPES]


def download_link(dir_link):
    directory, link = dir_link
    download_path = directory / os.path.basename(link)
    with urlopen(link) as image, download_path.open('wb') as f:
        f.write(image.read())
    logger.info('Downloaded %s', link)


def setup_download_dir():
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir