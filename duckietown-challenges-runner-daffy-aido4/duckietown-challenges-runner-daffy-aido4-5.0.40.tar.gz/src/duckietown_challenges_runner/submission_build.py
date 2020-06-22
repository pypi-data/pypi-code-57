# coding=utf-8
import os
import subprocess
from . import dclogger

def build_image(client, path: str, tag: str, dockerfile: str, no_build: bool, no_cache:bool=False):
    if not no_build:
        cmd = ["docker", "build", "--pull", "-t", tag, "-f", dockerfile]
        if no_cache:
            cmd.append("--no-cache")
        with open(dockerfile) as _:
            contents = _.read()
        vnames = ['AIDO_REGISTRY', 'PIP_INDEX_URL']
        for vname in vnames:
            if vname in contents:
                value = os.environ.get(vname)
                cmd.append(['--build-arg', f'{vname}={value}'])
        cmd.append(path)

        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            dclogger.error(f'Cannot run {cmd}')
            dclogger.error(e.stderr)
            raise

    image = client.images.get(tag)
    return image
