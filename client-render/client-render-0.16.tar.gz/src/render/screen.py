import logging
import sys
import time
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


if __name__ == '__main__':
    delay = int(sys.argv[1])
    process = Process(
        target=capture_screenshots,
        args=(delay,),
        name="Make screenshots"
    )
    process.daemon = True
    process.start()
    logger.info(f"Process was started with {process.pid}")
