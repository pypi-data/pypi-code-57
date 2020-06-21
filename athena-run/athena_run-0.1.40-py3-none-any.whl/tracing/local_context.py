from collections import deque
from . import config

import uuid
import json
import random
import logging
from urllib import request, parse

log = logging.getLogger(__name__)


def _make_request(url, data):
    data = data.encode("utf-8")
    req = request.Request(url, data=data)
    req.add_header("Content-Type", "application/json")
    resp = request.urlopen(req)


def _print_trace_urls(traces):
    if len(traces["traces"]) > 0:
        for trace in traces["traces"]:
            log.warning(
                "Access the trace for your execution on Athena: %s",
                "http://app.athena-ml.com/traces/{}".format(trace["id"]),
            )


class LocalContext(object):
    """
    Class that stores context about the current nested set of traces
    It keeps track of parent-child relationships

    If a span exists, it has a corresponding empty child map
    """

    def __init__(
        self,
        trace_id=None,
        span_id=None,
        service="Default",
        dry_run=False,
        file_output=None,
    ):
        if span_id is None:
            span_id = random.getrandbits(32)

        if trace_id is None:
            trace_id = random.getrandbits(32)

        self.trace_id = trace_id
        self.child_map = {}
        self.spans_by_id = {}
        self.ordered_trace_deque = deque([span_id])
        self.child_map[span_id] = []
        self.service = service
        self.trace_buffer = {self.trace_id: []}

        self._file_output = file_output
        self._dry_run = dry_run

    def get_current_span_from_parent_tree(self):
        """
        Returns the trace that is currently at the lowest level
        in the dependency tree
        :return:
        """
        return self.ordered_trace_deque[-1]

    def remove_current_span_from_parent_tree(self):
        """
        Removes a trace from the lowest level of the dependency tree.
        :return:
        """
        self.ordered_trace_deque.pop()

    def add_new_span_to_parent_tree(self, new_trace=None):
        if new_trace is None:
            new_trace = random.getrandbits(32)
        self.child_map[new_trace] = []
        self.child_map[self.get_current_span_from_parent_tree()].append(new_trace)
        self.ordered_trace_deque.append(new_trace)

    def add_span_to_trace_buffer(self, span_record: config.SPAN_RECORD):
        span_as_map = config.convert_span_record_to_key_value(span_record)
        self.trace_buffer[self.trace_id].append(span_as_map)
        self.spans_by_id[span_as_map["span_id"]] = span_as_map

        if len(self.trace_buffer[self.trace_id]) >= config.DEFAULT_REQUEST_BUFFER_SIZE:
            self.flush_buffer_to_agent()

    def _get_fully_described_child(self, child):
        span_as_map = self.spans_by_id[child]
        span_as_map["id"] = span_as_map["span_id"]
        span_as_map["children"] = [
            self._get_fully_described_child(child) for child in span_as_map["children"]
        ]

        return span_as_map

    def _get_fully_described_trace(self, trace):
        # find the root span
        root = None

        for span in trace:
            if span["parent_id"] == 0:
                root = span
                break

        if not root:
            raise Exception("no root found for trace %s" % trace)

        root["children"] = [
            self._get_fully_described_child(child) for child in root["children"]
        ]
        root["meta"] = {"layer": "sigmoid", "neurons": 4, "next_layer": "curvilinear"}
        root["id"] = root["span_id"]

        return root

    def close_auto_main_span(self):
        from athena.patch.statsd_config import DEFAULT_STATSD_CLIENT as stats
        if hasattr(stats, '_main_timer'):
            stats._main_timer.stop()

    def stop_metrics_thread(self):
        from athena.patch.statsd_config import DEFAULT_STATSD_CLIENT as stats
        if hasattr(stats, '_metrics_stop'):
            stats._metrics_stop.set()

    def flush_buffer_to_agent(self):
        # Trace payload should look like
        # { "traces": [ { "id': "xyz", "trace": {} }, ...  ] }

        trace_list = {"traces": []}

        for trace_id, trace in self.trace_buffer.items():
            if len(trace) > 0:
                trace_list["traces"].append(
                    {"id": trace_id, "trace": self._get_fully_described_trace(trace)}
                )

        log.debug("submitting to Athena: %s", trace_list)
        if not self._dry_run:
            try:
                _make_request(config.DEFAULT_AGENT_URL, json.dumps(trace_list))
            except Exception as e:
                log.error("Failed to submit trace: %s", e)
        else:
            log.info("Dry run mode. Not submitting trace")
            if self._file_output:
                with open(self._file_output, "w") as out:
                    log.info("writing trace to %s", self._file_output)
                    json.dump(trace_list, out)

        if not self._dry_run:
            _print_trace_urls(trace_list)
        self.trace_buffer.clear()
        self.trace_buffer[self.trace_id] = []
