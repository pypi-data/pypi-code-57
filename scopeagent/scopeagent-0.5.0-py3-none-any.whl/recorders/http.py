import gzip
import io
import logging
import uuid

import certifi
import msgpack

import urllib3

from .asyncrecorder import AsyncRecorder
from ..formatters.dict import DictFormatter
from ..tracer import tags
from .utils import UnrecoverableClientError, RecoverableClientError

logger = logging.getLogger(__name__)

INGEST_NUM_RETRIES = 10
INGEST_TIMEOUT = 10

MAXIMUM_NUMBER_OF_SPANS_TO_INGEST = 1000
MAXIMUM_NUMBER_OF_EVENTS_TO_INGEST = 1000


class HTTPRecorder(AsyncRecorder):
    def __init__(self, api_key, api_endpoint, metadata=None, dry_run=False, **kwargs):
        super(HTTPRecorder, self).__init__(**kwargs)
        self._api_key = api_key
        self._api_endpoint = api_endpoint
        self._ingest_endpoint = "%s/%s" % (self._api_endpoint, 'api/agent/ingest')
        self.metadata = metadata or {}
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        self.dry_run = dry_run
        self._spans_left_to_send = []
        self._events_left_to_send = []
        self._metadata_sent = False
        self._unfinished_spans = {}
        self._ingest_has_failed = False

    @staticmethod
    def _is_recoverable_http_error(http_error_status):
        return http_error_status >= 500 and http_error_status != 501

    def record_unfinished_span(self, span):
        self._unfinished_spans[span.context.span_id] = span

    def remove_unfinished_span(self, span):
        self._unfinished_spans.pop(span.context.span_id)

    def mark_unfinished_spans(self):
        for span in self._unfinished_spans.values():
            span.set_tag(tags.UNFINISHED, True)

    def _send_payload(self):
        payload = {
            "agent.id": self.metadata[tags.AGENT_ID],
            "spans": [],
            "events": [],
        }
        if not self._metadata_sent:
            payload['metadata'] = self.metadata

        if self._ingest_has_failed:
            payload['control'] = {tags.INGEST_ERROR: True}

        payload['spans'] = self._spans_left_to_send[:MAXIMUM_NUMBER_OF_SPANS_TO_INGEST]
        payload['events'] = self._events_left_to_send[:MAXIMUM_NUMBER_OF_EVENTS_TO_INGEST]
        logger.debug('sending payload to server: %s', payload)
        self._send(payload)
        self._spans_left_to_send = self._spans_left_to_send[MAXIMUM_NUMBER_OF_SPANS_TO_INGEST:]
        self._events_left_to_send = self._events_left_to_send[MAXIMUM_NUMBER_OF_EVENTS_TO_INGEST:]

    def flush_final_payload(self):
        self.mark_unfinished_spans()
        self.flush(self._unfinished_spans.values())
        while len(self._spans_left_to_send) > 0 or len(self._events_left_to_send) > 0:
            self._send_payload()
        final_payload = {
            "control": {tags.PROCESS_END: True},
            "agent.id": self.metadata[tags.AGENT_ID],
            "spans": [],
            "events": [],
        }
        if self._ingest_has_failed:
            final_payload['control'][tags.INGEST_ERROR] = True

        self._send(final_payload)

    def flush(self, spans):
        for span in spans:
            span_dict = DictFormatter.dumps(span)
            events = span_dict.pop('logs')
            self._spans_left_to_send.append(span_dict)
            span_context = span_dict['context']
            for event in events:
                event['context'] = {
                    'trace_id': span_context['trace_id'],
                    'span_id': span_context['span_id'],
                    'event_id': str(uuid.uuid4()),
                }
                self._events_left_to_send.append(event)

        self._send_payload()

    def _send(self, body):
        from .. import version

        payload_msgpack = msgpack.dumps(body, default=lambda value: str(value))
        logger.debug("uncompressed msgpack payload size is %d bytes", len(payload_msgpack))
        out = io.BytesIO()
        with gzip.GzipFile(fileobj=out, mode="wb") as f:
            f.write(payload_msgpack)
        payload_gzip = out.getvalue()
        logger.debug("compressed gzip payload size is %d bytes", len(payload_gzip))

        headers = {
            "User-Agent": "scope-agent-python/%s" % version,
            "Content-Type": "application/msgpack",
            "X-Scope-ApiKey": self._api_key,
            "Content-Encoding": "gzip",
        }
        if not self.dry_run:
            resp = self.http.request(
                'POST',
                self._ingest_endpoint,
                headers=headers,
                body=payload_gzip,
                retries=INGEST_NUM_RETRIES,
                timeout=INGEST_TIMEOUT,
            )
            if resp.status != 200:
                if self._is_recoverable_http_error(resp.status):
                    raise RecoverableClientError(resp)
                else:
                    self._ingest_has_failed = True
                    raise UnrecoverableClientError(resp)
            if not self._metadata_sent:
                self._metadata_sent = True

            logger.debug("response from server: %d %s", resp.status, resp.data)
        else:
            logger.debug("dry run active, payload not sent to server")
