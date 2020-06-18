import os
import time
import uuid
import json
import sys
import logging
import threading
import traceback
from io import StringIO
from logging.handlers import RotatingFileHandler
from datetime import datetime
from etools.utils import get_host_ip


if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else: #pragma: no cover
    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


class ElkRecord:
    class CommonInfo:
        def __init__(self, sn, env):
            self.sn = sn
            self.env = env
            self.host = get_host_ip()

    access_logger = None
    service_logger = None
    common_info = None

    @classmethod
    def enabled(cls):
        return cls.access_logger is not None and cls.common_info is not None

    @classmethod
    def init(cls, service_name, env, access_log_file, service_log_file):
        cls.common_info = cls.CommonInfo(service_name, env)
        access_logger = logging.getLogger("__elk_access__")
        access_logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(
                access_log_file, maxBytes=100 * 1024 * 1024, backupCount=10)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        access_logger.addHandler(handler)
        access_logger.propagate = False
        cls.access_logger = access_logger

        service_logger = logging.getLogger("__elk_service__")
        service_logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(
                service_log_file, maxBytes=100 * 1024 * 1024, backupCount=10)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        service_logger.addHandler(handler)
        service_logger.propagate = False
        cls.service_logger = service_logger

    def __init__(self,
                 rid=None,
                 uri=None,
                 domain=None,
                 client_ip=None,
                 user_agent=None,
                 method=None,
                 request_body=None):
        self.rid = rid or self.generate_uuid()
        self.access_time = time.time()
        self.method = method
        self.uri = uri
        self.domain = domain
        self.client_ip = client_ip
        self.user_agent = user_agent
        self.request_body = request_body
        if not isinstance(self.request_body, str):
            self.request_body = json.dumps(self.request_body, ensure_ascii=False)
        self.cost = None
        self.status = None
        self.response_body = None

    def generate_uuid(self):
        return str(uuid.uuid1()).replace("-", "")

    def end(self, response, status=None):
        self.cost = (time.time() - self.access_time) * 1000
        self.access_time = datetime.strftime(
                datetime.fromtimestamp(self.access_time),
                "%Y-%m-%d %H:%M:%S.%f")
        self.response_body = response
        if not isinstance(self.response_body, str):
            self.response_body = json.dumps(self.response_body, ensure_ascii=False)
        self.status = status
        self.access_logger.info(json.dumps({
            "sn": self.common_info.sn,
            "env": self.common_info.env,
            "host": self.common_info.host,
            "logId": self.generate_uuid(),
            "rid": self.rid,
            "accessTime": self.access_time,
            "method": self.method,
            "uri": self.uri,
            "domain": self.domain,
            "clientIp": self.client_ip,
            "userAgent": self.user_agent,
            "requestBody": self.request_body,
            "cost": self.cost,
            "status": self.status,
            "responseBody": self.response_body
        }, ensure_ascii=False))

    def debug(self, msg, *args):
        self._log("debug", msg, *args)

    def info(self, msg, *args):
        self._log("info", msg, *args)

    def warning(self, msg, *args):
        self._log("warning", msg, *args)

    def error(self, msg, *args):
        self._log("error", msg, *args)

    def exception(self, msg, *args):
        self._log("error", msg, *args)

    def _log(self, level, msg, *args):
        now = time.time()
        filename, lineno = self.find_caller()
        if args:
            msg = msg % args
        getattr(self.service_logger, level)(json.dumps({
            "sn": self.common_info.sn,
            "env": self.common_info.env,
            "host": self.common_info.host,
            "logId": self.generate_uuid(),
            "rid": self.rid,
            "time": datetime.strftime(
                datetime.fromtimestamp(now),
                "%Y-%m-%d %H:%M:%S.%f"),
            "filename": filename,
            "line": lineno,
            "msg": msg,
            "thread": threading.currentThread().ident,
            "level": level.upper(),
            "cost": now - self.access_time,
            "exception": self.get_exception_info()
        }, ensure_ascii=False))

    def find_caller(self):
        cur_file = os.path.normcase(__file__)
        try:
            f = currentframe()
            while hasattr(f, "f_code"):
                co = f.f_code
                filename = os.path.normcase(co.co_filename)
                if filename == cur_file:
                    f = f.f_back
                    continue
                return co.co_filename, f.f_lineno
        except Exception as e:
            return "unknown", 0

    def get_exception_info(self):
        t, v, tb = sys.exc_info()
        if t is None and v is None and tb is None:
            return None
        stringio = StringIO()
        traceback.print_exception(t, v, tb, None, stringio)
        return stringio.getvalue()
