#!/usr/bin/python
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Types shared between readers and reporters."""

from typing import Any, Dict, Iterable, List, Tuple, Union

# Currently a metric can only be keyed by a string. Prefixes can't act as
# dictionary keys as they're not hashable. We could consider opening this up to
# tuples as well.
MetricKey = str
Metric = Any

Prefix = Union[MetricKey, List[str]]
Suffix = Union[MetricKey, List[str]]
Attachment = Union[Prefix, Suffix]
