# Copyright (C) 2020 Esteban López Rodríguez <gnu_stallman@protonmail.ch>
#
# This file is part of Spike.
#
# Spike is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Spike is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from sys import argv
from os import listdir, getpid
from os.path import basename


def spike_pid():
    cmd = basename(argv[0])
    current = str(getpid())
    proc_list = [x for x in listdir("/proc") if x.isdigit() and x != current]

    for proc in proc_list:
        with open("/proc/" + proc + "/cmdline") as f:
            cmdline = f.readline()
        if cmd in cmdline:
            return proc

    return None

