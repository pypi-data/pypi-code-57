import logging
import traceback
import six
from datetime import datetime
from inspect import isclass, istraceback

from ..compat import utc
from .base import Formatter
from ..tracer import tags


logger = logging.getLogger(__name__)


class DictFormatter(Formatter):
    @classmethod
    def dumps(cls, span):
        ret = {
            'context': {
                'trace_id': '{0:032x}'.format(span.context.trace_id),
                'span_id': '{0:016x}'.format(span.context.span_id),
                'baggage': span.context.baggage or None,
            },
            'parent_span_id': "%x" % span.parent_id if span.parent_id else None,
            'operation': span.operation_name,
            'start': (datetime.fromtimestamp(span.start_time, tz=utc)).isoformat(),
            'duration': round(span.duration * 1e9),
            'tags': {k: cls._serialize_tag(k, v) for k, v in span.tags.items()} or None,
            'logs': [
                {
                    'timestamp': (datetime.fromtimestamp(log.timestamp, tz=utc)).isoformat(),
                    'fields': {k: cls._serialize_field(k, v) for k, v in log.key_values.items()},
                }
                for log in span.logs
            ],
        }
        logger.debug("formatting span %s", ret)
        return ret

    @classmethod
    def _serialize_field(cls, key, value):
        UNSAFE_EVENT_TAGS = [tags.MESSAGE]
        """Field values can include any JSON-serializable type"""
        if isclass(value):
            return value.__name__
        elif isinstance(value, Exception):
            return ''.join(traceback.format_exception_only(value.__class__, value)).strip()
        elif istraceback(value):
            return ''.join(traceback.format_tb(value)).strip()
        elif key in UNSAFE_EVENT_TAGS:
            return six.ensure_str(value)
        else:
            return value

    @classmethod
    def _serialize_tag(cls, key, value):
        UNSAFE_SPAN_TAGS = [tags.HTTP_REQUEST_PAYLOAD, tags.HTTP_RESPONSE_PAYLOAD]
        if key in UNSAFE_SPAN_TAGS:
            return six.ensure_str(value)
        return value
