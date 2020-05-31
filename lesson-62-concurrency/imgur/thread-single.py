
import os
from time import time

from downloader import setup_download_dir, get_links, download_link, get_logger

logger = get_logger(__name__)

def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir()
    links = get_links(client_id)
    for link in links:
        download_link((download_dir, link))
    logger.info(f'Downloading {len(links)} images took {time() - ts} seconds')

if __name__ == '__main__':
    main()