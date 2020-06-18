# -*- coding: utf-8 -*-
# pylint: disable=unused-import, unused-wildcard-import
"""library foundation

:mod:`pcapkit.foundation` is a collection of fundations for
:mod:`pcapkit`, including PCAP file extraction tool
:class:`~pcapkit.foundation.extraction.Extrator`, application
layer protocol analyser :class:`~pcapkit.foundation.analysis.Analysis`,
and TCP flow tracer :class:`~pcapkit.foundation.tractflow.TraceFlow`.

"""
from pcapkit.foundation.analysis import analyse as analyse2
from pcapkit.foundation.extraction import *
from pcapkit.foundation.traceflow import *

__all__ = ['analyse2', 'Extractor', 'TraceFlow']
