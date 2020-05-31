
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
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
    dir_links = [(download_dir, link) for link in links]

    # By placing the executor inside a with block, the executors shutdown method
    # will be called cleaning up threads.
    # 
    # By default, the executor sets number of workers to 5 times the number of
    # CPUs.
    with ThreadPoolExecutor() as executor:

        # Executes fn concurrently using threads on the links iterable. The
        # timeout is for the entire process, not a single call, so downloading
        # all images must complete within 30 seconds.
        executor.map(download_link, dir_links, timeout=30)

    logger.info(f'Downloading {len(links)} images took {time() - ts} seconds')


if __name__ == '__main__':
    main()