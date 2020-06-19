import argparse
import os
import json
from os import PathLike
from pathlib import Path
from typing import NoReturn, Optional
from alive_progress import alive_bar
from docker import DockerClient
from docker.api.client import DockerException
from docker.types import Mount
from docker.models.images import Image
from docker.models.containers import Container
from .decorators import auto_remove, progress_gen


parser = argparse.ArgumentParser(description="gvmkit image builder")
parser.add_argument(
    "--info", "-i", action="store_true", help="extract container information only"
)
parser.add_argument("image", type=str, help="docker image identifier")
parser.add_argument("--output", type=str, help= "output file name")
parser.add_argument('--version', action='version', version=f'%(prog)s 0.1.3')


class Converter:
    DEFAULT_SQUASHFS_IMAGE = "prekucki/squashfs-tools:latest"
    SCRIPT_INPUT = "/work/in"
    SCRIPT_OUTPUT = "/work/out/image.squashfs"
    DEFAULT_SCRIPT = (
        f"mksquashfs {SCRIPT_INPUT} {SCRIPT_OUTPUT} -info -comp lzo -noappend"
    )

    def __init__(self, client: DockerClient, output_file: PathLike):
        self._client = client
        self._image = fetch_image(client, self.DEFAULT_SQUASHFS_IMAGE)
        self._output_file = output_file

    def __enter__(self):
        work_file = os.path.abspath(self._output_file)
        # truncate file
        with open(work_file, "wb"):
            pass
        script = self.DEFAULT_SCRIPT
        self._tool: Optional[Container] = self._client.containers.create(
            self._image,
            command=script,
            mounts=[
                Mount(target=Converter.SCRIPT_OUTPUT, source=work_file, type="bind")
            ],
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tool.remove(force=True)

    def add_image(self, image: Image):
        assert self._tool is not None
        tool = self._tool
        with auto_remove(self._client.containers.create(image)) as src, alive_bar(
            title="extracting files"
        ) as bar:
            tool.put_archive(Converter.SCRIPT_INPUT, progress_gen(bar, src.export()))

    def add_text_file(self, container_path: str, content: str):
        import tarfile
        import io
        buffer = io.BytesIO()
        t = tarfile.open(fileobj=buffer, mode='w')
        entry = tarfile.TarInfo(container_path)
        content_bytes = content.encode('utf-8')
        entry.size = len(content_bytes)
        t.addfile(entry, fileobj=io.BytesIO(content_bytes))
        t.close()
        tar_bytes = buffer.getvalue()
        assert self._tool is not None
        self._tool.put_archive(self.SCRIPT_INPUT, tar_bytes)

    def convert(self):
        assert self._tool is not None
        tool = self._tool

        with alive_bar(title="packing files") as bar:
            tool.start()
            bar()
            for line in tool.logs(stream=True):
                bar(line.decode("unicode_escape"))
            bar()
            tool.wait()


def build():
    args = parser.parse_args()
    client = DockerClient.from_env()

    image = fetch_image(client, args.image)
    config = image.attrs["Config"]
    meta = {}
    print(json.dumps(config, indent=4))
    for key in [ "Env", 'Cmd', "Entrypoint" ]:
        if config[key]:
            meta[key.lower()] = config[key]

    if args.info:
        print(json.dumps(meta, indent=4))
        return
    output_file = args.output or f"image-{image.id}"
    with Converter(client, output_file) as builder:
        builder.add_image(image)
        for key, contents in meta.items():
            contents = '\n'.join(contents) + '\n'
            builder.add_text_file(f".{key}", contents)
        builder.convert()


def fetch_image(client: DockerClient, image_id: str) -> Image:
    try:
        image = client.images.get(image_id)
        if image:
            return image
    except DockerException:
        pass
    parts = *image_id.split(":"), ""
    name, tag, *_ = parts

    with alive_bar(title=f"pull {name}:{tag}") as bar:
        tag = tag or "latest"
        bar()
        return client.images.pull(name, tag)
