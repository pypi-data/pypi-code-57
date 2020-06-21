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

from markupsafe import Markup

from fresco import context
from fresco_flash import FlashMiddleware


def info(message):
    context.request.environ[FlashMiddleware.env_key](
        message, FlashMiddleware.INFO
    )


def warn(message):
    context.request.environ[FlashMiddleware.env_key](
        message, FlashMiddleware.WARN
    )


def error(message):
    context.request.environ[FlashMiddleware.env_key](
        message, FlashMiddleware.ERROR
    )


def messages():
    """
    Return a list of (level, message) tuples flashed from the previous request
    """
    return [
        (l, Markup(m))
        for l, m in context.request.environ[FlashMiddleware.env_key_messages]
    ]
