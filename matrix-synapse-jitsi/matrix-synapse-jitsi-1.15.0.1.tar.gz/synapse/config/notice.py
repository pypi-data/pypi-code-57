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

from ._base import Config


class NoticeConfig(Config):
    section = "notice"

    def read_config(self, config, **kwargs):
        self.notice_url = config.get("notice_url")
        self.notice_key = config.get("notice_key")

    def generate_config_section(self, **kwargs):
        return """\
        ## Notice ##

        # The url and key for notice server
        #
        #notice_url: "https://notice.example.com"
        #notice_key: "example_key"
        """
