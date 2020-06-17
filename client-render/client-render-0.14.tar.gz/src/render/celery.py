import logging
import os
import time
from multiprocessing import Process
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT

from celery import Celery
from mss import mss

celery = Celery()
celery.config_from_object('render.celeryconfig')

logger = logging.getLogger(__name__)

render_dir = Path('c:') / 'render'


def capture_screenshots(path=render_dir / 'screens'):
    os.makedirs(path, exist_ok=True)
    i = 0
    while True:
        with mss() as sct:
            filename = f'{i}.png'
            sct.shot(output=str(path / filename))
            logger.debug(f"Screen {filename} is captured")

            time.sleep(1 * 60)  # screen each 1 minute

        i += 1


def render(*files):
    os.makedirs(render_dir / '1', exist_ok=True)  # fixup
    os.makedirs(render_dir / '2', exist_ok=True)  # fixup

    process = Popen([
        "c:\\program files\\autodesk\\3ds Max 2018\\3dsmaxcmd",
        "-continueOnError",
        "-batchRender",
        str(render_dir / '1-1.max')
    ],
        stderr=STDOUT,
        stdout=PIPE,
        bufsize=1,
    )

    log_dir = render_dir / 'logs'
    with open(log_dir / 'rendering.log', 'wb') as f:
        for s in process.stdout:
            f.write(s)
            if b'\r' in s or b'\n' in s:
                f.flush()  # flush only with end of line

    process.wait()
    if process.returncode > 0:
        raise Exception(f"3dsmax returned non zero code {process.returncode}")


@celery.task(name="run")
def run(*files):
    Process(target=capture_screenshots).start()
    # p.join()
    render(*files)
    # if p.exit_code >= 0:
    #    raise Exception(f"Process finised with {p.exit_code}")
