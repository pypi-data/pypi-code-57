# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""File Provider Input Connection class."""
from typing import Optional, TYPE_CHECKING

from ayx_plugin_sdk.core.doc_utilities import inherit_docs
from ayx_plugin_sdk.core.input_connection_base import InputConnectionBase
from ayx_plugin_sdk.core.metadata import Metadata
from ayx_plugin_sdk.core.record_packet import RecordPacket

import pandas as pd


if TYPE_CHECKING:
    from ayx_plugin_sdk.providers.file_provider.file_provider_input_anchor import (
        FileProviderInputAnchor,
    )


@inherit_docs
class FileProviderInputConnection(InputConnectionBase):
    """An input connection contains incoming record and metadata information."""

    def __init__(
        self,
        name: str,
        metadata: Metadata,
        packet: Optional[RecordPacket] = None,
        anchor: Optional["FileProviderInputAnchor"] = None,
    ) -> None:
        """
        Instantiate a file provider input connection.

        Parameters
        ----------
        name
            Name of the input connection.
        metadata
            Metadata for the input connections.
        packet
            Record information for the input connection.
        """
        if packet and packet.metadata != metadata:
            raise ValueError(
                "Record packet metadata must be the same as anchor metadata."
            )

        self.__packet = packet
        self.__name = name
        self.__metadata = metadata
        self.__anchor = anchor
        self.max_packet_size = None

    @property
    def name(self) -> str:  # noqa: D102
        return self.__name

    @property
    def metadata(self) -> Optional[Metadata]:  # noqa: D102
        return self.__metadata

    @property
    def anchor(self) -> "FileProviderInputAnchor":  # noqa: D102
        if self.__anchor:
            return self.__anchor

        raise RuntimeError("This input connection is not associated with an anchor.")

    def read(self) -> RecordPacket:  # noqa: D102
        if self.metadata is None:
            raise ValueError("Metadata must be set.")

        return self.__packet or RecordPacket(
            self.metadata, pd.DataFrame(columns=[field.name for field in self.metadata])
        )

    @property
    def max_packet_size(self) -> Optional[int]:  # noqa: D102
        return self.__max_packet_size

    @max_packet_size.setter
    def max_packet_size(self, value: Optional[int]) -> None:
        """
        Max packet size in the file provider should always be None.

        Otherwise, a user could try and set max packet size for the file provider and would not know why it was not affecting their tool.
        """
        if value is None:
            self.__max_packet_size = value
        else:
            raise ValueError("max_packet_size must be None in the file provider.")
