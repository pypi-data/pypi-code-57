import logging
import os
import sys
import time
from functools import partial
from multiprocessing import Process

from mss import mss

from render import RENDER_DIR

logger = logging.getLogger(__name__)


def capture_screenshots(delay):
    logger.debug("Screenshots configuring...")
    path = RENDER_DIR / 'screens'
    path.mkdir(exist_ok=True)
    i = 0
    while True:
        with mss() as sct:
            filename = f'{i}.png'
            sct.shot(output=str(path / filename))
            logger.debug(f"Screen {filename} is captured")

            time.sleep(delay * 60)

        i += 1


def main():

    delay = int(sys.argv[1])
    capture_screenshots(delay)
    # process = Process(
    #     target=partial(capture_screenshots, delay),
    # )
    # process.daemon = True
    # process.start()
    # process.join()
    # print(f"Process was started with {process.pid}")


if __name__ == '__main__':
    main()
