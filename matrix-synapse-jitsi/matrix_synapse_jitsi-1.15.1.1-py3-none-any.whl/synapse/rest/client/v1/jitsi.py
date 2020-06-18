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


class JitsiRestServlet(RestServlet):
    PATTERNS = client_patterns("/jitsi/rtcServer$", v1=True)

    def __init__(self, hs):
        super(JitsiRestServlet, self).__init__()
        self.hs = hs
        self.auth = hs.get_auth()

    async def on_GET(self, request):
        requester = await self.auth.get_user_by_req(request)

        jitsiUrl = self.hs.config.jitsi_url
        jitsiAppID = self.hs.config.jitsi_app_id
        jitsiAppSecret = self.hs.config.jitsi_app_secret

        return (
            200,
            {
                "url": jitsiUrl,
            },
        )

    def on_OPTIONS(self, request):
        return 200, {}


def register_servlets(hs, http_server):
    JitsiRestServlet(hs).register(http_server)
