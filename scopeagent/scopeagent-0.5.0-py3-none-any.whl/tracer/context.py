"""
Originally derived from https://github.com/opentracing/basictracer-python.
"""
from __future__ import absolute_import

import opentracing


class SpanContext(opentracing.SpanContext):
    """SpanContext satisfies the opentracing.SpanContext contract.

    span_id's range is [0, 2^SPAN_ID_LENGTH).
    trace_id's range is [0, 2^TRACE_ID_LENGTH).
    """

    def __init__(self, trace_id=None, span_id=None, baggage=None, sampled=True):
        self.trace_id = trace_id
        self.span_id = span_id
        self.sampled = sampled
        self._baggage = baggage or opentracing.SpanContext.EMPTY_BAGGAGE

    @property
    def baggage(self):
        return self._baggage

    def with_baggage_item(self, key, value):
        new_baggage = self._baggage.copy()
        new_baggage[key] = value
        return SpanContext(trace_id=self.trace_id, span_id=self.span_id, sampled=self.sampled, baggage=new_baggage)
