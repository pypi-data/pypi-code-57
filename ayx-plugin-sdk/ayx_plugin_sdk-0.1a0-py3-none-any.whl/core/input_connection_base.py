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
"""InputConnection base class definition."""
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ayx_plugin_sdk.core.input_anchor_base import InputAnchorBase
    from ayx_plugin_sdk.core.metadata import Metadata  # noqa: F401
    from ayx_plugin_sdk.core.record_packet_base import RecordPacketBase


class InputConnectionBase(ABC):
    """Input connection that receives data from upstream tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the connection name.

        Returns
        -------
        str
            Name of the input connection.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def metadata(self) -> Optional["Metadata"]:
        """
        Get the connection metadata.

        Returns
        -------
        Metadata, optional
            The metadata associated with this input connection.

            This will return None when accessed before the input
            connection has been opened, since the metadata isn't
            known until that point.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def anchor(self) -> "InputAnchorBase":
        """
        Get the input anchor this connection is associated with.

        Returns
        -------
        InputAnchorBase
            The anchor this input connection is associated with.
        """
        raise NotImplementedError()

    @abstractmethod
    def read(self) -> "RecordPacketBase":
        """
        Read a record packet from the incoming connection.

        Returns
        -------
        RecordPacketBase
            A record packet containing the data received by this connection.
        """
        raise NotImplementedError()

    @property  # type: ignore
    @abstractmethod
    def max_packet_size(self) -> Optional[int]:
        """
        Get the maximum number of records per packet.

        Returns
        -------
        int, optional
            The maximum number of records in a packet.
        """
        raise NotImplementedError()

    @max_packet_size.setter  # type: ignore
    @abstractmethod
    def max_packet_size(self, value: Optional[int]) -> None:
        """
        Set the maximum number of records per packet.

        Parameters
        ----------
        value
            The maximum number of records.
        """
        raise NotImplementedError()
