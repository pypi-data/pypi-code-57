###############################################################################
# (c) Copyright 2020 CERN for the benefit of the LHCb collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import logging
from pathlib import Path
from os import mkdir
from os.path import exists

def set_up_logging(verbosity):
    verbosity = verbosity*10

    logFormatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-5.5s]  %(message)s")

    log_file = "{0}/{1}.log".format('./logs', 'lb-dev')

    if not exists('./logs'):
        mkdir('./logs')

    Path(log_file).touch(exist_ok=True)

    fileHandler = logging.FileHandler(log_file)
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)

    rootLogger = logging.getLogger()
    rootLogger.addHandler(fileHandler)
    rootLogger.setLevel(logging.DEBUG)

    if verbosity != 0 and verbosity <= 60:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        consoleHandler.level = 60 - verbosity
        rootLogger.addHandler(consoleHandler)

    