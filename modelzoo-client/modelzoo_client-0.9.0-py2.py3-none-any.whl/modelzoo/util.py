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

import io
import pathlib

import names
import tqdm


BASE_UI_URL = "http://app.modelzoo.dev"


def generate_model_name():
    return names.get_full_name().lower().replace(" ", "-")


def pretty_print_request(req):
    """
    Print a requests.PreparedRequest object to a string.

    https://stackoverflow.com/a/23816211
    """

    return "{}\r\n{}\r\n\r\n{}".format(
        req.method + " " + req.url,
        "\r\n".join("{}: {}".format(k, v) for k, v in req.headers.items()),
        req.body,
    )


def valid_file(path) -> bool:
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)

    return not (
        path.is_symlink()
        or path.is_socket()
        or path.is_fifo()
        or path.is_block_device()
        or path.is_char_device()
    )


class ProgressTracking:
    """
    Wraps an io.BufferedReader object such that the total progress of the read
    stream is output to a progress bar.

    Example usage:

        total_bytes = path.stat().st_size
        with path.open("rb") as f:
            progressf = ProgressTracking(total_bytes, f)
            requests.put(..., data=progressf)
    """

    def __init__(self, total_bytes: int, reader: io.BufferedReader):
        self.total_bytes = total_bytes
        self.progress_bar = tqdm.tqdm(
            iterable=None,
            total=total_bytes,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )
        self.reader = reader

    def read(self, size=-1):
        self.progress_bar.update(size)
        return self.reader.read(size)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        else:
            return getattr(self.reader, attr)
