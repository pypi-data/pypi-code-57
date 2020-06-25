# -*- coding: utf-8 -*-
# Copyright 2014-2016 OpenMarket Ltd
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

import base64
import hashlib
import hmac

from synapse.http.servlet import RestServlet
from synapse.rest.client.v2_alpha._base import client_patterns


class NoticeRestServlet(RestServlet):
    PATTERNS = client_patterns("/notice/bulletinBoard$", v1=True)

    def __init__(self, hs):
        super(NoticeRestServlet, self).__init__()
        self.hs = hs
        self.auth = hs.get_auth()
        self.http_client = hs.get_simple_http_client()

    async def on_GET(self, request):
        requester = await self.auth.get_user_by_req(request)

        noticeUrl = self.hs.config.notice_url
        noticeKey = self.hs.config.notice_key

        response = await self.http_client.get_json(noticeUrl, args={"key": noticeKey})

        return (
            200,
            {
                "data": response["data"],
            },
        )

    def on_OPTIONS(self, request):
        return 200, {}


def register_servlets(hs, http_server):
    NoticeRestServlet(hs).register(http_server)
