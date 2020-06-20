#!/usr/bin/python3
#
#  constants.py
#
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import os
import pathlib
from typing import Union

# 3rd party
import importlib_resources  # type: ignore
import magic  # type: ignore
from typing_extensions import Literal

# this package
from wx_icons_hicolor import Hicolor

__all__ = ["mime", "theme_index_path", "PathLike", "IconTypes"]

mime = magic.Magic(mime=True)

with importlib_resources.path(Hicolor, "index.theme") as theme_index_path:
	theme_index_path = pathlib.Path(theme_index_path)

PathLike = Union[str, pathlib.Path, os.PathLike]
IconTypes = Literal["Fixed", "Scalable", "Threshold"]
