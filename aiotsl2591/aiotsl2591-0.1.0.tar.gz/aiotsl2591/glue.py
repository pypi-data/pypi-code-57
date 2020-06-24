#
# aiotsl2591 - TSL2591 sensor asyncio library
#
# Copyright (C) 2020 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
TSL2591 sensor communication interface.
"""

import asyncio
import operator

from ._aiotsl2591 import tsl2591_init, tsl2591_read_start, tsl2591_read_end, \
    tsl2591_close

extract = operator.attrgetter('pressure', 'temperature', 'humidity')

class Sensor:
    """
    TSL2591 sensor communication interface.
    """
    def __init__(self, f_dev, address):
        """
        Initialize sensor.

        :param f_dev: I2C device filename, i.e. /dev/i2c-0.
        :param address: I2C device address, i.e. 0x77.
        """
        self._data = tsl2591_init(f_dev.encode(), address)
        self._loop = asyncio.get_event_loop()
        self._loop.add_reader(self._data.timer_fd, self._process_event)

    async def read(self):
        """
        Read pressure, temperature and humidity from sensor.

        The method is a coroutine.

        The returned sensor data is a tuple of pressure, temperature and
        humidity values.
        """
        tsl2591_read_start(self._data)
        task = self._task = self._loop.create_future()
        return (await task)

    def close(self):
        """
        Release resources claimed by sensor.
        """
        tsl2591_close(self._data)

        task = self._task
        if task and not task.done():
            task.cancel()
            self._task = None

    def _process_event(self):
        """
        Finish asynchronous call reading sensor data.
        """
        data = self._data
        tsl2591_read_end(data)
        self._task.set_result(data.lux)
        self._task = None

# vim: sw=4:et:ai
