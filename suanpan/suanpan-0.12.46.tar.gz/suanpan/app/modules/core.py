# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.app import app
from suanpan.app.modules.base import Module


module = Module()


@module.fn
def notifyError(err, *args, **kwargs):
    app.sio.error(err, *args, **kwargs)
