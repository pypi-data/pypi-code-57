from etornado.buildin_handlers.base_handler import BaseHandler
from etornado.error_code_manager import ErrorCode, ErrorCodeException


class UnsupportedUrlHandler(BaseHandler):

    async def do_process(self, *args, **kwargs):
        ec_exception = ErrorCodeException(ErrorCode.UNSUPPORTED_URL,
                                          {"url": self.request.uri})
        return ec_exception, None
