# Copyright 2019 Cognite AS
import logging
import os
import time

import grpc
from grpc._channel import (
    _InactiveRpcError,
    _SingleThreadedUnaryStreamMultiCallable,
    _StreamStreamMultiCallable,
    _UnaryStreamMultiCallable,
    _UnaryUnaryMultiCallable,
)

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos import ingest_service_pb2_grpc as ingest_serv
    from cognite.seismic.protos import query_service_pb2_grpc as query_serv
    from cognite.seismic._api.file import FileAPI
    from cognite.seismic._api.job import JobAPI
    from cognite.seismic._api.slice import SliceAPI
    from cognite.seismic._api.survey import SurveyAPI
    from cognite.seismic._api.time_slice import TimeSliceAPI
    from cognite.seismic._api.trace import TraceAPI
    from cognite.seismic._api.volume import VolumeAPI


# The maximum number of retries
_MAX_RETRIES_BY_CODE = {
    grpc.StatusCode.INTERNAL: 1,
    grpc.StatusCode.ABORTED: 3,
    grpc.StatusCode.UNAVAILABLE: 5,
    grpc.StatusCode.DEADLINE_EXCEEDED: 5,
}

# The minimum seconds (float) of sleeping
_MIN_SLEEPING = 0.1
_MAX_SLEEPING = 5.0

logger = logging.getLogger(__name__)


class RetriesExceeded(Exception):
    """docstring for RetriesExceeded"""

    pass


def retry(f, transactional=False):
    def wraps(*args, **kwargs):
        retries = 0
        while True:
            try:
                return f(*args, **kwargs)
            except _InactiveRpcError as e:
                code = e.code()

                max_retries = _MAX_RETRIES_BY_CODE.get(code)
                if max_retries is None or transactional and code == grpc.StatusCode.ABORTED:
                    raise

                if retries > max_retries:
                    raise RetriesExceeded(e)

                backoff = min(_MIN_SLEEPING * 2 ** retries, _MAX_SLEEPING)
                logger.info("sleeping %r for %r before retrying failed request...", backoff, code)

                retries += 1
                time.sleep(backoff)

    return wraps


def retrying_stub_methods(obj):
    for key, attr in obj.__dict__.items():
        if (
            isinstance(attr, _UnaryUnaryMultiCallable)
            or isinstance(attr, _StreamStreamMultiCallable)
            or isinstance(attr, _UnaryStreamMultiCallable)
            or isinstance(attr, _SingleThreadedUnaryStreamMultiCallable)
        ):
            setattr(obj, key, retry(attr))


class CogniteSeismicClient:
    """
    Main class for the seismic client
    """

    def __init__(self, api_key=None, base_url=None, port=None):
        # configure env
        self.api_key = api_key or os.getenv("COGNITE_API_KEY")
        if self.api_key is None or self.api_key == "":
            raise ValueError(
                "You have either not passed an api key or not set the COGNITE_API_KEY environment variable."
            )
        self.base_url = base_url or "api.cognitedata.com"
        self.port = port or "443"
        self.url = self.base_url + ":" + str(self.port)
        self.metadata = [("api-key", self.api_key)]

        # start the connection
        credentials = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(
            self.url,
            credentials,
            options=[
                ("grpc.max_receive_message_length", 10 * 1024 * 1024),
                ("grpc.keepalive_time_ms", 5000),
                ("grpc.keepalive_permit_without_calls", 1),
                ("grpc.http2.max_pings_without_data", 0),
                ("grpc.http2.min_time_between_pings_ms", 5000),
            ],
        )
        self.query = query_serv.QueryStub(channel)
        self.ingestion = ingest_serv.IngestStub(channel)
        retrying_stub_methods(self.query)
        retrying_stub_methods(self.ingestion)

        self.survey = SurveyAPI(self.query, self.ingestion, self.metadata)
        self.file = FileAPI(self.query, self.ingestion, self.metadata)
        self.trace = TraceAPI(self.query, self.metadata)
        self.slice = SliceAPI(self.query, self.metadata)
        self.volume = VolumeAPI(self.query, self.metadata)
        self.time_slice = TimeSliceAPI(self.query, self.metadata)
        self.job = JobAPI(self.ingestion, self.metadata)
