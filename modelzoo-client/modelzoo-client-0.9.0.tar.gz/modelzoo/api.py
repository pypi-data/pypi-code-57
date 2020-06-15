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
import platform
import requests
import typing
import urllib.parse
import sys
from typing import Any

from . import config, util, __version__


class APIError(Exception):
    pass


def raw_call(
    method: str, path: str, api_key: typing.Optional[str] = None, payload: Any = None,
) -> Any:
    response = requests.request(
        method=method,
        url=urllib.parse.urljoin(config.get_base_api_url(), path),
        json=payload,
        headers={
            "x-api-key": config.get_api_key(api_key),
            "x-modelzoo-client-type": "python-client",
            "x-modelzoo-client-python-version": sys.version.replace("\n", " "),
            "x-modelzoo-client-platform": platform.version(),
            "x-modelzoo-client-version": __version__.get(),
        },
    )
    logging.debug(
        "HTTP Request:\n{}".format(util.pretty_print_request(response.request))
    )
    logging.debug(
        "HTTP Response:\n({}) {}".format(response.status_code, response.content)
    )

    return response


def call(
    method: str, path: str, api_key: typing.Optional[str] = None, payload: Any = None,
) -> Any:
    response = raw_call(method, path, api_key, payload)

    if response.headers.get("content-type") == "application/json":
        body = response.json()
    elif response.headers.get("content-type") == "text/plain":
        body = response.text
    else:
        body = response.content

    if response.status_code >= 400:
        raise APIError(str(body))

    return body


def upload_file(filelike: Any, presigned_url: str) -> Any:
    response = requests.put(presigned_url, data=filelike)
    if response.status_code >= 400:
        raise APIError(response.text)
    return response.content
