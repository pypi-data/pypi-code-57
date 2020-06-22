# PyAlgoTrade
#
# Copyright 2011-2018 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

import logging
import threading

initLock = threading.Lock()
rootLoggerInitialized = False

log_format = "%(asctime)s %(name)s [%(levelname)s] %(message)s"
simpleLog_format = "%(message)s"

level = logging.INFO
file_log = None  # File name
console_log = True



def getFileLogger(name,fileName,mode_='w'):

    aLog= logging.getLogger(name)
    aLog.propagate=False
    if not aLog.hasHandlers():
        aLog.setLevel(logging.INFO)
        fileHandler = logging.FileHandler(fileName,mode=mode_)
        fileHandler.setFormatter(logging.Formatter(simpleLog_format))
        aLog.addHandler(fileHandler)
    return aLog

def closeHandler(name):

    aLog= logging.getLogger(name)
    aLog.propagate=False

    while(1):
        if aLog.hasHandlers():


            aLog.removeHandler(aLog.handlers[0])
        else:
            break


