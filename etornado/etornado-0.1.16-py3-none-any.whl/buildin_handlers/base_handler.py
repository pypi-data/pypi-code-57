import json
import logging
import inspect
import uuid
from enum import Enum
from tornado.web import RequestHandler
from etornado.error_code_manager import ErrorCode, error_code_manager, ErrorCodeException
from etools.elk_record import ElkRecord


class AggregateHttMethodMeta(type):

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.head = cls.process
        cls.get = cls.process
        cls.post = cls.process
        cls.delete = cls.process
        cls.patch = cls.process
        cls.put = cls.process
        cls.options = cls.process


class BaseHandler(RequestHandler, metaclass=AggregateHttMethodMeta):

    def initialize(self, **kwargs):
        self.logger = logging.getLogger(self.__class__.__name__)
        for k, v in kwargs.items():
            if hasattr(self, k):
                self.logger.exception("member [%s] has exists", k)
                raise Exception("member [%s] has exists" % k)
            setattr(self, k, v)
        self.url_args = []
        self.elk_record = None
        self.rid = None
        self.log_request_body = True

    async def process(self, *args, **kwargs):
        self.rid = self.request.headers.get(
                "X-Request-Id", str(uuid.uuid1()).replace("-", ""))
        self.elk_record = self.create_elk_record()
        self.send_response_and_finish(*await self.do_process(*args, **kwargs))

    def write_error(self, status_code, **kwargs):
        self.send_response_and_finish(ErrorCodeException(ErrorCode.UNKNOWN))

    def send_response_and_finish(self, ec_exception, results=None):
        response = error_code_manager.format_error_info(
                ec_exception.error_code, **ec_exception.error_info)
        response["rid"] = self.rid
        if ec_exception.error_code == ErrorCode.NONE and results is not None:
            response["results"] = results
        response_body = json.dumps({"response": response}, ensure_ascii=False)
        if self.elk_record:
            self.elk_record.end(response_body, 200)
        self.write(response_body)
        self.finish()

    def create_elk_record(self):
        if not ElkRecord.enabled():
            return None
        request_body = self.request.body.decode("utf8") if self.log_request_body else None
        return ElkRecord(
                    rid = self.rid,
                    uri = self.request.uri,
                    domain = self.request.host,
                    client_ip = self.request.remote_ip,
                    user_agent = self.request.headers.get("User-Agent"),
                    method = self.request.method.upper(),
                    request_body = request_body)

    async def do_process(self, *args, **kwargs):
        method = getattr(self, "do_" + self.request.method.lower(), None)
        self.url_args = args
        ec_exception = ErrorCodeException(ErrorCode.NONE)
        results = None
        request_body = self.request.body.decode("utf8") if self.log_request_body else None
        if method is None:
            ec_exception = ErrorCodeException(
                    ErrorCode.UNSUPPORTED_METHOD,
                    {"method": self.request.method, "url": self.request.uri})
        else:
            try:
                results = method()
                if inspect.isawaitable(results):
                    results = await results
            except ErrorCodeException as e:
                self.logger.exception("rid[%s] error_code_exception [%s] catched when call [%s],"\
                                      " request[%s], request body[%s]",
                                      self.rid, e, method, self.request, request_body)
                ec_exception = e
            except Exception as e:
                self.logger.exception("rid[%s] exception [%s] catched when call [%s],"\
                                      " request[%s], request body[%s]",
                                      self.rid, e, method, self.request, request_body)
                ec_exception = ErrorCodeException(ErrorCode.UNKNOWN)
        return ec_exception, results
