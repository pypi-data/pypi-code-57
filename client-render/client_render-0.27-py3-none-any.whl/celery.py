import glob
import itertools
import logging
import os
import re
import shutil
from datetime import datetime
from logging import DEBUG
from pathlib import Path, PurePosixPath
from subprocess import Popen, PIPE, STDOUT

from celery import Celery

from render import RENDER_DIR
import render.aws as aws
from render.logger import configure_logger

celery = Celery()
celery.config_from_object('render.celeryconfig')

logger = logging.getLogger(__name__)


class FollowLog:
    BATCH_RENDER_NAME = re.compile(r'Batch render job being rendered:(.*)')
    COMPLETE = re.compile(r'Job Complete - Results in')

    def __init__(self, workdir: Path, extension: str):
        self.buffer = []
        self.current_view = self.next_handler = None
        assert workdir
        assert extension
        self.workdir = workdir
        self.extension = extension

        self.handlers = itertools.cycle([
            self.BATCH_RENDER_NAME, self.COMPLETE
        ])
        self.next()

    def clear(self):
        self.buffer = []

    @property
    def to_str(self):
        return ''.join(self.buffer)

    def next(self):
        self.clear()
        self.next_handler = next(self.handlers)
        logger.info(f'Following pattern "{self.next_handler.pattern}"')

    def make_view_dir(self):
        directory = self.workdir / self.current_view
        directory.mkdir(exist_ok=True)
        logger.info(f"Created directory - {directory}")

    def move_files(self):
        assert self.current_view
        dest_directory = self.workdir / self.current_view
        pattern = str(self.workdir / f'*.{self.extension}')
        for file in glob.glob(pattern):
            filename = os.path.basename(file)
            dst_filename = dest_directory / filename
            shutil.move(file, dst_filename)
            logger.info(f"File {filename} moved into {dest_directory}")

            yield dst_filename

    def process(self, s):
        self.buffer.append(s)
        matched = self.next_handler.search(self.to_str)
        if matched:
            if self.next_handler == self.BATCH_RENDER_NAME:
                self.current_view = matched.group(1).strip()
                self.make_view_dir()

            if self.next_handler == self.COMPLETE:
                yield from self.move_files()

            self.next()

    def iterate_files(self, stdout):
        # noinspection PyTypeChecker
        with open(self.workdir / 'rendering.log', 'wb') as f:
            for s in stdout:
                # remove ASCII NULL symbol
                part = s.replace(b'\x00', b'')
                f.write(part)
                f.flush()

                yield from self.process(part.decode())


class Scene:
    def __init__(self, scene: str):
        self.path = PurePosixPath(scene)

    @property
    def task_id(self):
        return self.path.parent

    @property
    def workdir(self):
        directory = RENDER_DIR / self.task_id.name
        directory.mkdir(exist_ok=True)
        return directory

    @property
    def filename(self):
        return self.path.name

    @property
    def localfile(self):
        return self.workdir / 'scene' / self.filename


class Render:
    def __init__(self, scene: Scene, client: aws.S3):
        self.scene = scene
        self.client = client

    def run(self, extension='exr'):
        self.client.download_file(self.scene.path, self.scene.localfile)
        logger.info(f"Scene downloaded - {self.scene.localfile}")
        if not self.scene.localfile.is_file():
            raise Exception("Local file does not exists")

        max_cmd = Path(os.environ['ADSK_3DSMAX_x64_2018']) / '3dsmaxcmd'
        process = Popen([
            str(max_cmd),
            "-continueOnError",
            "-batchRender",
            f'-outputName:{str(self.scene.workdir / f"0.{extension}")}',
            str(self.scene.localfile)],
            stderr=STDOUT,
            stdout=PIPE,
            bufsize=1,
        )

        follow = FollowLog(self.scene.workdir, extension)
        for file in follow.iterate_files(process.stdout):
            view = file.parent.name
            self.client.upload_file(
                self.scene.task_id / 'result' / view / file.name,
                file
            )
            logger.info(f"Artifact is uploaded - {file}")
        process.wait()
        return process.returncode


def record_time(f):
    def format_date(value: datetime):
        return value.strftime('%H:%M:%S %d-%m-%Y')

    def wrapper(*args, **kwargs):
        begin = datetime.now()
        logger.info(f"Rendering is started!")
        try:
            return f(*args, **kwargs)
        finally:
            end = datetime.now()
            logger.info(f"Rendering is finished!")
            logger.info(f"Took: {str(end - begin).split('.')[0]}")

    return wrapper


def collect_logs(scene: Scene, client: aws.S3):
    logger.info("Collecting log files...")
    for file in itertools.chain(
            # additional logs could be appended here
            glob.glob(str(Path(os.environ['LOG_DIR']) / '*.log')),
            glob.glob(str(scene.workdir / '*.log')),
    ):
        logger.info(f"Found log {file}")
        client.upload_file(
            scene.task_id / 'logs' / os.path.basename(file),
            file
        )


def run(scene_key):
    assert os.environ['ADSK_3DSMAX_x64_2018'], "ADSK_3DSMAX_x64_2018 must be defined"
    assert os.environ['AWS_ACCESS_KEY_ID'], "AWS_ACCESS_KEY_ID must be defined"
    assert os.environ['AWS_SECRET_ACCESS_KEY'], "AWS_SECRET_ACCESS_KEY must be defined"
    assert os.environ['AWS_ENDPOINT'], "AWS_ENDPOINT must be defined"
    assert os.environ['AWS_BUCKET'], "AWS_BUCKET must be defined"
    assert os.environ['LOG_DIR'], "LOG_DIR must be defined"
    s3 = aws.S3(
        os.environ['AWS_BUCKET'],
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        endpoint_url=os.environ['AWS_ENDPOINT'],
    )
    scene = Scene(scene_key)
    # configure current logger for the specific scene
    configure_logger(scene.workdir, level=logging.getLevelName(DEBUG))

    render = Render(scene, client=s3)
    try:
        rc = record_time(render.run)()
        if rc > 0:
            raise Exception(f"3dsmax returned non zero code {rc}")
    except Exception as e:
        logger.exception(e)
        raise
    finally:
        collect_logs(scene, s3)


@celery.task(name="run")
def main(*args, **kwargs):
    run(*args, **kwargs)
