import logging
import os
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT

from celery import Celery

from render import RENDER_DIR

celery = Celery()
celery.config_from_object('render.celeryconfig')

logger = logging.getLogger(__name__)


def render(*files):
    os.makedirs(RENDER_DIR / '1', exist_ok=True)  # fixup
    os.makedirs(RENDER_DIR / '2', exist_ok=True)  # fixup

    max_cmd = Path(os.environ['ADSK_3DSMAX_x64_2018']) / '3dsmaxcmd'
    process = Popen([
        str(max_cmd),
        "-continueOnError",
        "-batchRender",
        str(RENDER_DIR / '1-1.max')
    ],
        stderr=STDOUT,
        stdout=PIPE,
        bufsize=1,
    )

    log_dir = Path(os.environ['LOG_DIR'])
    with open(log_dir / 'rendering.log', 'wb') as f:
        for s in process.stdout:
            # remove ascii symbols shortly
            f.write(s.replace(b'\x00', b''))
            f.flush()

    process.wait()
    return process.returncode


@celery.task(name="run")
def run(*files):
    assert os.environ['ADSK_3DSMAX_x64_2018'], "ADSK_3DSMAX_x64_2018 must be defined"
    assert os.environ['LOG_DIR'], "LOG_DIR must be defined"
    assert os.environ['AWS_ACCESS_KEY_ID'], "AWS_ACCESS_KEY_ID must be defined"
    assert os.environ['AWS_SECRET_ACCESS_KEY'], "AWS_SECRET_ACCESS_KEY must be defined"
    assert os.environ['AWS_ENDPOINT'], "AWS_ENDPOINT must be defined"
    assert os.environ['AWS_BUCKET'], "AWS_BUCKET must be defined"

    rc = render(*files)
    if rc > 0:
        raise Exception(f"3dsmax returned non zero code {rc}")

    # if p.exit_code >= 0:
    #    raise Exception(f"Process finised with {p.exit_code}")
