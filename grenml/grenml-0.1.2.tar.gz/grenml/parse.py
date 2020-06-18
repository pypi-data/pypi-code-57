"""
Copyright 2020 CANARIE Inc.

SPDX-License-Identifier: Apache License 2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

--------------------------------------------------------------------

Synopsis: GRENML parser. This file provides the ability to parse files and
streams into a provided GRENML manager
"""

from grenml import GRENMLManager
from grenml.parsing import GRENMLHandler
import xml.sax
from io import StringIO


class GRENMLParser:
    """
    Controller to manage parsing GRENML from streams as well as files
    """

    def __init__(self):
        self.parser = xml.sax.make_parser()
        self.handler = GRENMLHandler()
        self.parser.setContentHandler(self.handler)

    def parse_stream(self, stream) -> GRENMLManager:
        self.parser.parse(stream)
        return self.handler.manager

    def parse_string(self, string) -> GRENMLManager:
        return self.parse_stream(StringIO(string))

    def parse_file(self, file_name) -> GRENMLManager:
        return self.parse_stream(open(file_name, 'r'))
