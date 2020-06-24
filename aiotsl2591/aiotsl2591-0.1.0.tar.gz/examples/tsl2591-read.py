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

import argparse
import asyncio
import aiotsl2591
import logging
import time
import uvloop

from datetime import datetime
from functools import partial

logging.basicConfig(level=logging.DEBUG)

async def read_data(dev, addr):
    sensor = aiotsl2591.Sensor(dev, addr)

    fmt = '{} ({:.4f}): {:.2f}lx'.format
    while True:
        t1 = time.monotonic()
        lux = await sensor.read()
        t2 = time.monotonic()

        print(fmt(datetime.now(), t2 - t1, lux))
        await asyncio.sleep(1)

parser = argparse.ArgumentParser(description='TSL2591 sensor example')
parser.add_argument('device', help='I2C device filename, i.e. /dev/i2c-0')
parser.add_argument(
    'address', type=partial(int, base=16),
    help='I2C device address, i.e. 0x29 (hex value)'
)
args = parser.parse_args()

uvloop.install()
asyncio.run(read_data(args.device, args.address))

# vim: sw=4:et:ai
