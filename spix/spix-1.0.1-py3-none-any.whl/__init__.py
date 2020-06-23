# Copyright 2020 Louis Paternault
#
# This file is part of SpiX.
#
# SpiX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SpiX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SpiX.  If not, see <https://www.gnu.org/licenses/>.

"""Compile a `.tex` file, executing commands that are set inside the file itself."""

import os
import pathlib
import re
import subprocess

NAME = "SpiX"
VERSION = "1.0.1"

RE_EMPTY = re.compile("^ *$")
RE_COMMENT = re.compile("^ *%")
RE_COMMAND = re.compile(r"^%\$ ?(.*)$")


def parse_lines(lines):
    """Parse line to find code snippets.

    :param iterable lines: Lines to parte (typically ``open("foo.tex").readlines()``.
    :return: Iterator over snippets (as strings).
    """
    snippet = None
    for line in lines:
        line = line.rstrip("\n")
        if RE_COMMAND.match(line):
            match = RE_COMMAND.match(line)
            if snippet is None:
                snippet = ""
            else:
                snippet += "\n"
            snippet += match.groups()[0]
        elif RE_EMPTY.match(line) or RE_COMMENT.match(line):
            if snippet is not None:
                yield snippet
                snippet = None
        else:
            break
    if snippet is not None:
        yield snippet


class SpixError(Exception):
    """Exception that should be catched and nicely displayed to user."""


def compiletex(filename, *, dryrun=False):
    """Read commands from file, and execute them.

    :param str filename: File to process.
    :param bool dryrun: If ``True``, print commands to run, but do not execute them.
    """
    env = os.environ
    filename = pathlib.PosixPath(filename)
    env["texname"] = filename.name
    env["basename"] = filename.stem

    try:
        with open(filename, errors="ignore") as file:
            for snippet in parse_lines(file.readlines()):
                print(snippet)
                if dryrun:
                    continue

                subprocess.check_call(
                    ["sh", "-c", snippet, NAME, filename.name],
                    cwd=(pathlib.Path.cwd() / filename).parent,
                    env=env,
                )
    except subprocess.CalledProcessError:
        raise SpixError()
    except IsADirectoryError as error:
        raise SpixError(str(error))
