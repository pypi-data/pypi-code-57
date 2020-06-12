# -*- coding: utf-8 -*-

# Copyright 2018-2020 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Store files in ZIP archives"""

from .common import PostProcessor
from .. import util
import zipfile


class ZipPP(PostProcessor):

    COMPRESSION_ALGORITHMS = {
        "store": zipfile.ZIP_STORED,
        "zip"  : zipfile.ZIP_DEFLATED,
        "bzip2": zipfile.ZIP_BZIP2,
        "lzma" : zipfile.ZIP_LZMA,
    }

    def __init__(self, job, options):
        PostProcessor.__init__(self, job)
        self.delete = not options.get("keep-files", False)
        ext = "." + options.get("extension", "zip")
        algorithm = options.get("compression", "store")
        if algorithm not in self.COMPRESSION_ALGORITHMS:
            self.log.warning(
                "unknown compression algorithm '%s'; falling back to 'store'",
                algorithm)
            algorithm = "store"

        self.path = job.pathfmt.realdirectory
        args = (self.path[:-1] + ext, "a",
                self.COMPRESSION_ALGORITHMS[algorithm], True)

        if options.get("mode") == "safe":
            self.run = self._write_safe
            self.zfile = None
            self.args = args
        else:
            self.run = self._write
            self.zfile = zipfile.ZipFile(*args)

    def _write(self, pathfmt, zfile=None):
        # 'NameToInfo' is not officially documented, but it's available
        # for all supported Python versions and using it directly is a lot
        # faster than calling getinfo()
        if zfile is None:
            zfile = self.zfile
        if pathfmt.filename not in zfile.NameToInfo:
            zfile.write(pathfmt.temppath, pathfmt.filename)
            pathfmt.delete = self.delete

    def _write_safe(self, pathfmt):
        with zipfile.ZipFile(*self.args) as zfile:
            self._write(pathfmt, zfile)

    def run_final(self, pathfmt, status):
        if self.zfile:
            self.zfile.close()

        if self.delete:
            util.remove_directory(self.path)

            if self.zfile and not self.zfile.NameToInfo:
                # remove empty zip archive
                util.remove_file(self.zfile.filename)


__postprocessor__ = ZipPP
