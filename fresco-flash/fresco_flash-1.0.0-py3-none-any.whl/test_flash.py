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

from json import dumps
from markupsafe import Markup, escape

from fresco import FrescoApp, context, GET, Response
from fresco_flash import FlashMiddleware, flash


def flash_messages():
    request = context.request
    for item in request.query.getlist("m"):
        flash.info(item)
    if "r" in request.query:
        return Response.redirect(request.query.get("r"))
    return Response([dumps(flash.messages())])


app = FrescoApp()
app.route("/flash", GET, flash_messages)
app.add_middleware(FlashMiddleware)


def doflash(*messages):
    with app.requestcontext():
        for m in messages:
            flash.info(m)
        return flash.messages()


def doflash_cross_request(*messages):
    def flashit_and_redirect(environ, start_response):
        for m in messages:
            flash.info(m)
        start_response("302 Found", [("location", "/")])
        return []

    def start_response(status, headers, exc_info=None):
        start_response.status = status
        start_response.headers = headers

    with app.requestcontext() as c:
        FlashMiddleware(flashit_and_redirect)(c.request.environ, start_response)
        cookie = dict(start_response.headers)["Set-Cookie"]
        cookie = cookie.split(";", 1)[0]

    with app.requestcontext(HTTP_COOKIE=cookie) as c:
        wsgiapp = FlashMiddleware(lambda *args, **kwargs: [])
        wsgiapp(c.request.environ, start_response)
        return flash.messages()


def doflash_one(message):
    return doflash(message)[0][1]


def doflash_one_cross_request(message):
    return doflash_cross_request(message)[0][1]


class TestFlash(object):
    def test_flash(self):
        assert doflash("hello") == [("INFO", Markup("hello"))]

    def test_flash_with_redirect(self):
        assert doflash_cross_request("hello") == [("INFO", Markup("hello"))]

    def test_multi_flash_with_redirect(self):
        assert doflash_cross_request("hello", "world") == [
            ("INFO", Markup("hello")),
            ("INFO", Markup("world")),
        ]

    def test_multi_flash_with_metachars_and_redirect(self):
        assert doflash_cross_request("hel:lo", "wo,r;ld") == [
            ("INFO", Markup("hel:lo")),
            ("INFO", Markup("wo,r;ld")),
        ]


class TestEscaping(object):
    def test_it_escapes_embedded_html(self):

        with app.requestcontext("/"):
            flash.info("2 > 1")
            assert flash.messages() == [("INFO", "2 &gt; 1")]

    def test_it_preserves_untainted_markup(self):

        with app.requestcontext("/"):
            flash.info(Markup("2 > 1"))
            assert flash.messages() == [("INFO", "2 > 1")]

    def test_it_preserves_tainting_info(self):

        msg = doflash_one_cross_request("2 > 1")
        assert str(escape(msg)) == "2 &gt; 1"

        msg = doflash_one_cross_request(Markup("2 > 1"))
        assert str(escape(msg)) == "2 > 1"
