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


class NotifyConfig(Config):
    section = "notify"

    def read_config(self, config, **kwargs):
        self.notify_url = config.get("notify_url")
        self.notify_debug_url = config.get("notify_debug_url")

    def generate_config_section(self, **kwargs):
        return """\
        ## Notify ##

        # The url for notify server
        #
        #notify_url: "https://notify.example.com"
        #notify_debug_url: "https://notify_debug.example.com"
        """
