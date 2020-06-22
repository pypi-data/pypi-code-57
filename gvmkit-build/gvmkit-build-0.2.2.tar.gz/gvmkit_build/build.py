import argparse
import json
import os
import sys
from os import PathLike
from pathlib import Path
from contextlib import suppress
from typing import Optional, List
from typing_extensions import Final
import re

import alive_progress as ap
from alive_progress import alive_bar
from docker import DockerClient
from docker.api.client import DockerException
from docker.models.containers import Container
from docker.models.images import Image
from docker.types import Mount
from yaml_dump import yaml_dump

from .decorators import auto_remove, progress_gen
from . import gvmi
from pkg_resources import get_distribution


VERSION: Final = get_distribution("gvmkit-build").version
parser = argparse.ArgumentParser(
    prog="gvmkit-build", description="gvmkit image builder",
)
parser.add_argument(
    "--info", "-i", action="store_true", help="extract container information only"
)
parser.add_argument("image", type=str, help="docker image identifier")
parser.add_argument("--output", "-o", type=str, help="output file name")
parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
parser.add_argument("--vol", "-v", type=str, nargs="+", help="Additional mount points")
parser.add_argument(
    "--push", action="store_true", help="pushes image to application registry"
)

_WINDOWS = sys.platform == "win32"


class Converter:
    C_TYPE_LABEL: Final = "network.golem.gvmkit.ctype"

    DEFAULT_SQUASHFS_IMAGE: Final = "prekucki/squashfs-tools:latest"
    SCRIPT_INPUT: Final = "/work/in"
    SCRIPT_OUTPUT: Final = "/work/out/image.squashfs"
    DEFAULT_SCRIPT: Final = (
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
            labels={self.C_TYPE_LABEL: "converter"},
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tool.remove(force=True, v=True)

    def add_image(self, image: Image):
        assert self._tool is not None
        tool = self._tool
        with auto_remove(
            self._client.containers.create(image, labels={self.C_TYPE_LABEL: "src"})
        ) as src, alive_bar(title="extracting files") as bar:
            tool.put_archive(Converter.SCRIPT_INPUT, progress_gen(bar, src.export()))

    def add_text_file(self, container_path: str, content: str):
        import tarfile
        import io

        buffer = io.BytesIO()
        t = tarfile.open(fileobj=buffer, mode="w")
        entry = tarfile.TarInfo(container_path)
        content_bytes = content.encode("utf-8")
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
            for line_bytes in tool.logs(stream=True):
                # on windows long lines breaks formatting
                line = None if _WINDOWS else line_bytes.decode("unicode_escape")
                bar(line)
            bar()
            tool.wait()


def build():

    if _WINDOWS:
        ap.config_handler.set_global(theme="ascii")

    args = parser.parse_args()
    client = DockerClient.from_env()

    image = fetch_image(client, args.image)
    config = image.attrs["Config"]
    meta = {}
    print(f"Docker Image : {image.id}")
    print(
        f"Entry Point  : {' '.join(map(repr, config['Entrypoint'])) if config['Entrypoint'] else '<none>'}"
    )
    print(f"Working Dir  : {config['WorkingDir'] or '<none>'}")
    print(
        f"Command      : {' '.join(map(repr, config['Cmd'])) if config['Cmd'] else '<none>'}"
    )
    print(f"User         : {config['User'] or '<none>'}")
    vols = config["Volumes"]
    if isinstance(vols, dict):
        print(f"Volumes      :")
        print("")
        for vol in vols.keys():
            print(f"     - {vol}")
        print("")
    else:
        print(f"Volumes     : <none>")
    print(f"Env          :")
    print("")
    for env in config["Env"] or []:
        print(f"     - {env}")
    print("")

    for key in ["Env", "Cmd", "Entrypoint"]:
        if config[key]:
            meta[key.lower()] = config[key]

    output_file = args.output or default_output_file(image)
    print(f"Output File  : {output_file}")
    print("")
    if args.info:
        return

    config["GVMKIT"] = dict(
        generator="gvmkit-build-py",
        version=VERSION,
        os=sys.platform,
        python_ver=sys.version,
    )

    with suppress(gvmi.InvalidImageFormat, FileNotFoundError), open(
        output_file, "r+b"
    ) as f:
        current_config = gvmi.decode_meta(f)
        if current_config["Image"] == config["Image"]:
            print("image already generated")
            return

    with Converter(client, output_file) as builder:
        builder.add_image(image)
        for key, contents in meta.items():
            contents = "\n".join(contents) + "\n"
            builder.add_text_file(f".{key}", contents)
        builder.convert()
    with open(output_file, "r+b") as f:
        gvmi.encode_meta(f, config)


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


def default_output_file(image: Image) -> str:
    short_id = image.short_id[len("SHA256:") :]
    for tag in image.tags:
        match = re.match(r"((?P<repo>[^/]*)/)?(?P<name>[^:]*)(:(?P<tag>[^:]*))?", tag)
        if match:
            repo, name, tag = match.group("repo", "name", "tag")
            return f'{repo or "docker"}-{name}-{tag}-{short_id}.gvmi'
    return f"local-image-{short_id}.gvmi"
