# Copyright 2015 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from base64 import b64encode, b64decode
from functools import partial

from markupsafe import escape

from fresco import core, context


__version__ = "1.0.0"


class FlashMiddleware(object):
    """
    Middleware to facilitate setting and displaying messages to the user across
    an http redirect.

    Usage::

        from fresco import context, flash

        def app1():
            flash.info("Operation completed")
            flash.warn("1 warning encountered")
            return Response.redirect('/app2.html')

        app1 = FlashMiddleware(app1)

        def app2():
            return Response("<p>Message was: %s</p>" %
                            context.request.environ['fresco.flash_messages'])

    """

    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"

    __name__ = "FlashMiddleware"

    #: Key used to reference the middleware in the WSGI environ
    env_key = "fresco.flash"

    #: Key used for stash of messages in the WSGI environ
    env_key_messages = "fresco.flash.messages"

    #: Name for messages stored in cookies
    cookie_key = "_flash"

    def __init__(self, app):
        self.app = app
        try:
            self.request_class = core.request_class
        except AttributeError:
            self.request_class = None

    def _flash(self, messages, message, category=INFO):
        messages.append((category, escape(message)))

    def _start_response(
        self, environ, start_response, status, headers, exc_info=None
    ):
        messages = environ[self.env_key_messages]
        script_name = environ.get("SCRIPT_NAME", "") or "/"

        # Redirect response: set flash cookie so the messages are persisted to
        # the next request
        if status[:2] == "30" and messages:
            cookie = ",".join(
                b64encode(("%s:%s" % (c, m)).encode("utf8")).decode("ascii")
                for c, m in messages
            )
            headers.append(
                (
                    "Set-Cookie",
                    "%s=%s;path=%s" % (self.cookie_key, cookie, script_name,),
                )
            )

        # Clear the cookie so that messages are not repeated on subsequent
        # requests
        elif self.cookie_key in environ.get("HTTP_COOKIE", ""):
            headers.append(
                (
                    "Set-Cookie",
                    "%s=;Expires=Tue, 01 Jan 1980 00:00:00;Path=%s"
                    % (self.cookie_key, script_name),
                )
            )

        return start_response(status, headers, exc_info)

    def __call__(self, environ, start_response):

        environ[self.env_key_messages] = messages = []
        environ[self.env_key] = partial(self._flash, messages)

        if self.cookie_key in environ.get("HTTP_COOKIE", ""):
            if self.request_class is None:
                self.request_class = context.app.request_class
            request = self.request_class(environ)
            cookie = request.cookies.get(self.cookie_key, None)
            if cookie:
                messages.extend(
                    b64decode(item.encode("ascii")).decode("utf8").split(":", 1)
                    for item in cookie.split(",")
                )

        return self.app(
            environ, partial(self._start_response, environ, start_response)
        )
