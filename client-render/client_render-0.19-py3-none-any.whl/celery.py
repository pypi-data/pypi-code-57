import glob
import itertools
import logging
import os
import re
import shutil
from pathlib import Path, PurePath
from subprocess import Popen, PIPE, STDOUT

from celery import Celery

from render import RENDER_DIR
from render.aws import S3

celery = Celery()
celery.config_from_object('render.celeryconfig')

logger = logging.getLogger(__name__)


class FollowLog:
    BATCH_RENDER_NAME = re.compile(r'Batch render job being rendered:(.*)')
    COMPLETE = re.compile(r'Scene .* completed')

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
        print(f'Following pattern "{self.next_handler.pattern}"')

    def make_view_dir(self):
        directory = self.workdir / self.current_view
        directory.mkdir(exist_ok=True)
        print(f"Created directory - {directory}")

    def move_files(self):
        assert self.current_view
        dest_directory = self.workdir / self.current_view
        pattern = str(self.workdir / f'*.{self.extension}')
        for file in glob.glob(pattern):
            filename = os.path.basename(file)
            dst_filename = dest_directory / filename
            shutil.move(file, dst_filename)
            print(f"File {filename} moved into {dest_directory}")

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


class Render:
    def __init__(self, scene: PurePath, client):
        self.scene = scene
        self.client = client

    @property
    def task_key(self):
        return self.scene.parent.parent

    @property
    def workdir(self):
        directory = RENDER_DIR / self.task_key.name
        directory.mkdir(exist_ok=True)
        return directory

    @property
    def filename(self):
        return self.scene.name

    @property
    def local_scene(self):
        return self.workdir / 'scene' / self.filename

    def run(self, extension='exr'):
        self.client.download_file(self.scene, self.local_scene)
        print(f"Scene downloaded - {self.local_scene}")
        if not self.local_scene.is_file():
            raise Exception("Local file does not exists")

        max_cmd = Path(os.environ['ADSK_3DSMAX_x64_2018']) / '3dsmaxcmd'
        process = Popen([
            str(max_cmd),
            "-continueOnError",
            "-batchRender",
            f'-outputName:{str(self.workdir / f"0.{extension}")}',
            str(self.local_scene)],
            stderr=STDOUT,
            stdout=PIPE,
            bufsize=1,
        )

        follow = FollowLog(self.workdir, extension)
        for file in follow.iterate_files(process.stdout):
            view = file.parent.name
            self.client.upload_file(
                self.task_key / 'result' / view / file.name,
                file
            )
            print(f"Artifact is uploaded - {file}")
        process.wait()
        return process.returncode


def _run(scene):
    s3 = S3(
        os.environ['AWS_BUCKET'],
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        endpoint_url=os.environ['AWS_ENDPOINT'],
    )
    render = Render(PurePath(scene), client=s3)
    rc = render.run()
    if rc > 0:
        raise Exception(f"3dsmax returned non zero code {rc}")


@celery.task(name="run")
def run(scene):
    assert os.environ['ADSK_3DSMAX_x64_2018'], "ADSK_3DSMAX_x64_2018 must be defined"
    assert os.environ['AWS_ACCESS_KEY_ID'], "AWS_ACCESS_KEY_ID must be defined"
    assert os.environ['AWS_SECRET_ACCESS_KEY'], "AWS_SECRET_ACCESS_KEY must be defined"
    assert os.environ['AWS_ENDPOINT'], "AWS_ENDPOINT must be defined"
    assert os.environ['AWS_BUCKET'], "AWS_BUCKET must be defined"
    return _run(scene)
