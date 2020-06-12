# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
A wrapper around xml.dom.minidom that provides safe versions of its functions for use
within pybuilds
"""
import xml.dom.minidom as xdm
from xml.dom.minidom import (  # noqa  # pylint: disable=unused-import
    getDOMImplementation,
    Node,
)
from portmod.io_guard import _wrap_path_read

parse = _wrap_path_read(xdm.parse)
