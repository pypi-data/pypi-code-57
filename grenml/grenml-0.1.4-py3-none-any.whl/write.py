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

Synopsis: GRENML writer. This file should provide the functionality for
writing a GRENML manager as GRENML.
"""

from grenml.writing.grenml import TopologyWriter
import io


class GRENMLWriter:

    def __init__(self, manager):
        self.manager = manager

    def write_stream(self, stream):
        TopologyWriter(stream, True).write_element(self.manager.topology)

    def write_string(self) -> str:
        data = io.StringIO()
        self.write_stream(data)
        return data.getvalue()

    def write_file(self, file_name: str):
        self.write_stream(open(file_name, 'w'))
