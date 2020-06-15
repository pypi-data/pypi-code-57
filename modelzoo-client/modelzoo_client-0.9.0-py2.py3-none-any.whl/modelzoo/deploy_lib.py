#  Copyright (C) 2020 Servly AI.
#  See the LICENCE file distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import logging
import pathlib
from typing import Dict, Optional

from termcolor import colored

from . import api, exceptions, util, _start, ResourcesConfig


def _upload_files(model_dir: pathlib.Path, upload_urls: Dict[str, str]):
    for filename, presigned_url in upload_urls.items():
        fullpath = model_dir.joinpath(pathlib.Path(filename))
        print("Uploading {}...".format(fullpath))
        total_bytes = fullpath.stat().st_size
        with fullpath.open("rb") as f:
            progress = util.ProgressTracking(total_bytes=total_bytes, reader=f)
            api.upload_file(progress, presigned_url)


def deploy_from_dir(
    model_name: str,
    model_dir: str,
    api_key: Optional[str] = None,
    resources_config: Optional[ResourcesConfig] = None,
    wait_until_healthy: bool = True,
    **model_kwargs
) -> str:
    model_dir = pathlib.Path(model_dir)
    if not model_dir.is_dir():
        raise exceptions.InvalidArgumentError(
            "model_dir '{}' must be a directory".format(model_dir)
        )

    if not resources_config:
        resources_config = ResourcesConfig()

    response = api.call(
        method="POST",
        path="models/create",
        api_key=api_key,
        payload={
            "model_name": model_name,
            "model_files": list(_get_files(model_dir)),
            "resources_config": resources_config.to_json(),
            **model_kwargs,
        },
    )
    _upload_files(model_dir, response["upload_urls"])
    print("Uploaded files from '{}'".format(model_dir))

    model_url = "{}/models/{}".format(util.BASE_UI_URL, model_name)
    print("")
    print(colored("{} created: {}".format(model_name, model_url), "green"))
    print("")

    _start.start(model_name, wait=wait_until_healthy, api_key=api_key)

    return model_name


def _get_files(model_dir: pathlib.Path):
    """
    Given an input model directory, enumerate a list of all the regular files
    that exist in it's directory.

    Args:
        model_dir: A directory on the filesystem that contains all model files.

    Returns:
        List of UNIX-style string filepaths, relative to the model directory.
    """
    for path in model_dir.glob("**/*"):
        if path.is_dir():
            continue

        if not util.valid_file(path):
            logging.warning(
                "Ignoring invalid file type {} ({})".format(str(path), path.stat())
            )

        # The extra wrapper to PurePosixPath ensures the path is UNIX-style,
        # regardless of
        yield str(pathlib.PurePosixPath(path.relative_to(model_dir)))
