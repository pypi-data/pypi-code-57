# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from mercurial import pycompat


def print_heptapod_env(repo, *args, **kwargs):
    # repr() does the job for us to format the list
    # sysstr decodes from latin-1 (no failures), and we need to reencode
    # for ui.status
    repo.ui.status(repr(sorted(
        (pycompat.sysstr(k), pycompat.sysstr(v))
        for (k, v) in repo.ui.environ.items()
        if k.startswith(b'HEPTAPOD_'))).encode('latin-1'))
    return 0
