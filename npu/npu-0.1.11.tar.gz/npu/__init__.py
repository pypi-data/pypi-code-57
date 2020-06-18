"""
:synopsis: The main npu api
.. moduleauthor:: Naval Bhandari <naval@neuro-ai.co.uk>
"""

from .npu import api, predict, compile, train, export
from . import vision, optim, loss

api.__module__ = "npu"
predict.__module__ = "npu"
compile.__module__ = "npu"
train.__module__ = "npu"
export.__module__ = "npu"
