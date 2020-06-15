import io
import time
from uuid import uuid4

import wrapt

from hoss_agent.conf.constants import EVENT, HOST_BLACK_LIST
from hoss_agent.context import execution_context
from hoss_agent.utils import compat
from hoss_agent.utils.logging import get_logger
from hoss_agent.utils.read_proxy import ReadProxy

try:
    from httplib import HTTPConnection, HTTPSConnection, HTTPResponse
except ImportError as error:
    from http.client import HTTPConnection, HTTPSConnection, HTTPResponse

logger = get_logger("hoss_agent.instrumentaion.packages.httpclient_hooks")


def install(module):
    wrapt.wrap_function_wrapper(
        module,
        "HTTPConnection._send_request", _sendrequest,
    )
    wrapt.wrap_function_wrapper(
        module,
        "HTTPConnection.getresponse", getresponse,
    )
    wrapt.wrap_function_wrapper(
        module,
        "HTTPResponse.close", response_close,
    )


# hook into sendrequest and set up a partial event object.
# the event object is store in the HTTPConnection object itself so it can be referenced in getresponse below
#
def _sendrequest(wrapped, instance, args, kwargs):
    #(self, method, url, body=None, headers={}, encode_chunked=False):
    try:
        host = instance.host
        method, url, body, headers = args[0:4]
        client = execution_context.get_client()
        if client is None:
            return wrapped(*args, **kwargs)
        if host in HOST_BLACK_LIST:
            logger.debug('Host is in blacklist. Skipping')
            return wrapped(*args, **kwargs)

        port = instance.port
        default_port = instance.default_port
        real_url = url

        if not real_url.startswith(("http://", "https://")):
            real_url = "%s://%s%s%s" % (
                default_port == 443 and "https" or "http",
                host,
                port != default_port and ":%s" % port or "",
                url,
            )
        request_received_at = int(round(time.time() * 1000))

        headers = dict(headers)

        req_body = io.BytesIO()
        if body is not None:
            if isinstance(body, bytes):
                req_body.write(body)
            elif isinstance(body, str):
                req_body.write(body.encode("utf-8"))
            else:
                # body is probably a file so we want to create a proxy around it to read its content
                largs = list(args)
                if hasattr(body, "read"):
                    proxy = ReadProxy(body, req_body)
                    largs[2] = proxy
                    args = tuple(largs)

        instance._hoss_context = {
            "event": {
                "eventId": uuid4(),
                "request": {
                    "method": method,
                    "headers": headers,
                    "body": req_body,
                    "url": real_url,
                    "receivedAt": request_received_at
                }
            },
            "client": client
        }
    except Exception as ex:
        logger.debug('Error caught in monkey-patched http client send_request: %s', ex)

    return wrapped(*args, **kwargs)


# Hook into getresponse to further construct the event object that was started in _sendrequest.
# We can't read response body here because it'll close the body. We need to hook into HTTPResponse.read for that.
# So we have to save the event to the response object so when read is called, we can reference the event
def getresponse(wrapped, instance, args, kwargs):
    rv = wrapped(*args, **kwargs)
    try:
        hoss_context = getattr(instance, "_hoss_context", None)

        if hoss_context is None:
            return wrapped(*args, **kwargs)

        response_received_at = int(round(time.time() * 1000))

        if compat.PY2:
            # in python 2, HTTPResponse headers is a list of raw http header output, so turn them into a dict by splitting by : then
            # trimming \r\n
            headers = {c[0]: c[1][0:-2] for c in [h.split(': ') for h in rv.msg.headers]}
        else:
            headers = dict(rv.headers)
        hoss_context['event']['response'] = {
            "headers": headers,
            "statusCode": rv.status,
            "receivedAt": response_received_at,
            "body": io.BytesIO()
        }
        rv._hoss_context = hoss_context
    except Exception as ex:
        logger.debug('Error in monkey-patched getresponse: %s', ex)

    return rv


# Monkey-patched response close. We will do final preparation steps for the event, e.g. base64 encode and queue it
# todo: Handle the case when close is never called. See the note below
#    # NOTE: it is possible that we will not ever call self.close(). This
#     #       case occurs when will_close is TRUE, length is None, and we
#     #       read up to the last byte, but NOT past it.
#     #
#     # IMPLIES: if will_close is FALSE, then self.close() will ALWAYS be
#     #          called, meaning self.isclosed() is meaningful.
def response_close(wrapped, instance, args, kwargs):
    rv = wrapped(*args, **kwargs)
    try:
        hoss_context = getattr(instance, "_hoss_context", None)
        if hoss_context is None:
            return rv

        if 'queued' not in hoss_context['event']:
            hoss_context['event']['queued'] = True
            hoss_context['client'].queue(EVENT, hoss_context['event'])
    except Exception as ex:
        logger.debug('Error in monkey-patched response.close: %s', ex)

    return rv
