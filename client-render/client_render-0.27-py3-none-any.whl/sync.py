import logging
import os
import sys
import time
from pathlib import Path

import hashlib
from render import RENDER_DIR

logger = logging.getLogger(__name__)

EXTENSIONS = [
    'cxr',
    'exr',
    'fxr',
    'log',
    'png',
    'jpg',
    'jpeg',
    'jpe',
    'bmp',
    'hdr',
    'pic',
]


def sha256(filename):
    hash_ = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_.update(byte_block)
        return hash_.hexdigest()


def iterate_files():
    for root, dir, files in os.walk(RENDER_DIR):
        for file in files:
            *_, ext = file.rsplit('.', maxsplit=1)
            if ext in EXTENSIONS:
                yield Path(root) / file


def check_files():
    # for file in iterate_files():
    #     hex = sha256(file)
    pass



def main(delay):
    while True:
        check_files()
        time.sleep(60 * delay)


if __name__ == '__main__':
    main(int(sys.argv[1]))
