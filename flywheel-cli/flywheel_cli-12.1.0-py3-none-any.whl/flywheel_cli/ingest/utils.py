"""Ingest utility module"""
import collections
import datetime
import functools
import json
import logging
import os
import random
import string
import sys
from typing import Any, Optional, Tuple

import flywheel
import fs.filesize
import pytz
import sqlalchemy as sqla

from ..util import get_cli_version
from .. import sdk_impl
from . import config as C
from . import errors
from . import schemas as T

log = logging.getLogger(__name__)


def generate_ingest_label():
    """Generate random ingest operation label"""
    rand = random.SystemRandom()
    chars = string.ascii_uppercase + string.digits
    return "".join(rand.choice(chars) for _ in range(8))


def encode_json(obj: Any) -> Any:
    """JSON encode additional data types"""
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, datetime.datetime):
        if obj.tzinfo is None:
            obj = pytz.utc.localize(obj)
        return obj.astimezone(pytz.utc).isoformat()
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    # default serialization/raising otherwise
    raise TypeError(repr(obj) + " is not JSON serializable")


# pylint: disable=C0103
json_serializer = functools.partial(
    json.dumps,
    default=encode_json,
    separators=(",", ":"),
)


def get_path_el(c_type, context, use_labels=False):
    """Get the path element for container"""
    if c_type == "group":
        return context.get("_id")
    if use_labels:
        fields = ["label"]
    else:
        fields = ["_id", "label"]
    for field in fields:
        value = context.get(field)
        if not value:
            continue
        if field == "_id":
            return f"<id:{value}>"
        if field == "label":
            return value
    raise TypeError(f"Cannot get {c_type} path element from context {context}")


def init_sqla(
    db_url: str = "sqlite:///:memory:"
) -> Tuple[sqla.engine.Engine, sqla.orm.sessionmaker]:
    """Return configured sqla engine and session factory for DB url"""
    engine_kwargs = {"json_serializer": json_serializer}
    if db_url.startswith("sqlite://"):
        pool_cls = sqla.pool.StaticPool if ":memory:" in db_url else sqla.pool.NullPool
        engine_kwargs.update({
            "connect_args": {"check_same_thread": False},
            "poolclass": pool_cls,
        })
    else:
        # TODO migrate from deprecated postgres:// scheme to postgresql://
        # TODO enable connection pooling in workers / api
        engine_kwargs.update({
            "connect_args": {'connect_timeout': 10},
            "poolclass": sqla.pool.NullPool,
        })

    engine = sqla.create_engine(db_url, **engine_kwargs)
    sessionmaker = sqla.orm.sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    return engine, sessionmaker


def get_api_key() -> str:
    """Return current user's API key from config"""
    config = sdk_impl.load_config()
    if not config or not config.get("key"):
        print("Not logged in, please login using `fw login` and your API key", file=sys.stderr)
        sys.exit(1)
    return config["key"]


@functools.lru_cache(maxsize=16)
def get_sdk_client(api_key: str) -> flywheel.Client:
    """Cache and return SDK client for given API key"""
    log.debug(f"Creating SDK client for {api_key}")
    return SDKClient(api_key)


class SDKClient:
    """SDK client w/o version check and w/ request timeouts and signed url support"""

    def __init__(self, api_key: str):
        fw = flywheel.Client(api_key)
        fw.api_client.user_agent = f'Flywheel CLI/{get_cli_version()} ' + fw.api_client.user_agent

        # disable version check
        fw.api_client.set_version_check_fn(None)

        # set request timeouts
        request = fw.api_client.rest_client.session.request
        timeout = C.CONNECT_TIMEOUT, C.READ_TIMEOUT
        request_with_timeout = functools.partial(request, timeout=timeout)
        fw.api_client.rest_client.session.request = request_with_timeout

        # check signed url support
        config = fw.get_config()
        features = config.get("features")

        self.fw = fw
        self.session = fw.api_client.rest_client.session
        self.signed_url = features.get("signed_url") or config.get("signed_url")

    def __getattr__(self, name):
        """Pass-through attribute access to the original client"""
        return getattr(self.fw, name)

    def upload(self, cont_name, cont_id, filename, fileobj, metadata=None):
        """Upload file to container"""
        sdk_upload = getattr(self.fw, f"upload_file_to_{cont_name}")
        log.debug(f"Uploading {filename} to {cont_name}/{cont_id}")
        size = os.fstat(fileobj.fileno()).st_size
        if self.signed_url:
            self.signed_url_upload(cont_name, cont_id, filename, fileobj, metadata=metadata)
        else:
            filespec = flywheel.FileSpec(filename, fileobj)
            sdk_upload(cont_id, filespec, metadata=json_serializer(metadata))
        log.debug(f"Uploaded {filename} ({fs.filesize.traditional(size)})")

    def signed_url_upload(self, cont_name, cont_id, filename, fileobj, metadata=None):
        """Upload file to container using signed urls"""
        url = f"/{cont_name}s/{cont_id}/files"
        ticket, signed_url = self.create_upload_ticket(url, filename, metadata=metadata)
        log.debug(f"Using signed url {signed_url}")
        self.session.put(signed_url, data=fileobj)  # use api session
        self.call_api(url, "POST", query_params=[("ticket", ticket)])

    def create_upload_ticket(self, url, filename, metadata=None):
        """Create signed url upload ticket"""
        response = self.call_api(
            url,
            "POST",
            body={"metadata": metadata or {}, "filenames": [filename]},
            query_params=[("ticket", "")],
            response_type=object,
        )
        return response["ticket"], response["urls"][filename]

    def call_api(self, resource_path, method, **kwargs):
        """Call api with defaults set to enable accessing the json response"""
        kwargs.setdefault("auth_settings", ["ApiKey"])
        kwargs.setdefault("_return_http_data_only", True)
        kwargs.setdefault("_preload_content", True)
        return self.fw.api_client.call_api(resource_path, method, **kwargs)


class LRUCache:
    """Simple LRU cache"""

    def __init__(self, max_length=1000):
        self.cache = collections.OrderedDict()
        self.max_length = max_length

    def __setitem__(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        self.cache[key] = value
        if len(self.cache) > self.max_length:
            self.cache.popitem(last=False)

    def __getitem__(self, key):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        raise KeyError

    def get(self, key, default=None):
        """Get with default"""
        try:
            return self[key]
        except KeyError:
            return default


def get_fw_auth(
    api_key: str,
    fw_client: Optional[flywheel.Client] = None,
) -> T.FWAuth:
    """Return FWAuth on successful core auth, raise 403 Forbidden otherwise"""
    parts = api_key.rsplit(":", maxsplit=1)
    if len(parts) != 2:
        raise errors.AuthenticationError("Invalid api key format. Required format: <host>:<key>")
    host, key = parts

    if not fw_client:
        fw_client = get_sdk_client(api_key)
    else:
        # validate that the client has the same api_key
        client_key = fw_client.api_client.configuration.api_key['Authorization']
        assert key == client_key, "Client API key and api_key should be the same"

    # get user auth status using the sdk
    try:
        auth = fw_client.get_auth_status()
    except flywheel.ApiException:
        # TODO verify that the exception is as assumed
        raise errors.AuthenticationError("Invalid API key", 403)

    # check that the user has admin privileges
    # TODO lift restriction once review can warn about perm errors
    # TODO in turn add user == db.ingest.user check for non-admins
    if not auth.user_is_admin:
        raise errors.AuthenticationError("Admin access required", 403)

    return T.FWAuth(
        api_key=api_key,
        host=host,
        user=auth.origin.id,
        is_admin=auth.user_is_admin,
    )
