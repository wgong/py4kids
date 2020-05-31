
import os
from queue import Queue
from threading import Thread
from time import time

from downloader import setup_download_dir, get_links, download_link, get_logger

logger = get_logger(__name__)


class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            try:
                download_link(self.queue.get())
            finally:
                self.queue.task_done()


def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir()
    links = get_links(client_id)

    # Create a queue to communicate with the worker threads
    q = Queue()
    # Create 1 worker thread per CPU core
    for x in range(os.cpu_count()):
        worker = DownloadWorker(q)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for link in links:
        logger.info('Queueing {}'.format(link))
        q.put((download_dir, link))
    # Causes the main thread to wait for the queue to finish processing all the tasks
    q.join()
    logger.info(f'Downloading {len(links)} images took {time() - ts} seconds')

if __name__ == '__main__':
    main()