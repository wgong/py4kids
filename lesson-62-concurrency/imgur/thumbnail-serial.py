import logging
from pathlib import Path
from time import time
import os
import glob

from PIL import Image

from download import rm_thumbnail

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def create_thumbnail(size, path):
    """
    Creates a thumbnail of an image with the same name as image but with
    _thumbnail appended before the extension.  E.g.:

    >>> create_thumbnail((128, 128), 'image.jpg')

    A new thumbnail image is created with the name image_thumbnail.jpg

    :param size: A tuple of the width and height of the image
    :param path: The path to the image file
    :return: None
    """
    image = Image.open(path)
    image.thumbnail(size)
    path = Path(path)
    name = path.stem + '_thumbnail' + path.suffix
    thumbnail_path = path.with_name(name)
    image.save(thumbnail_path)




def main():
    rm_thumbnail()
    ts = time()
    for image_path in Path('images').iterdir():
        create_thumbnail((128, 128), image_path)
    logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    main()