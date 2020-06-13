#  Copyright 2020 Parakoopa
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.

from skytemple_files.common.types.data_handler import DataHandler
from skytemple_files.graphics.wan_wat.model import Wan


class WanHandler(DataHandler[Wan]):
    """Handler for Wat/Wan images. This interface is NOT stable."""
    @classmethod
    def deserialize(cls, data: bytes, **kwargs) -> Wan:
        return Wan(data)

    @classmethod
    def serialize(cls, data: Wan, **kwargs) -> bytes:
        raise NotImplementedError()
