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
from contextlib import contextmanager
from shutil import rmtree
from uuid import uuid1
from os import mkdir
from os.path import exists

class TemporaryDirecotryHandler:
    def __init__(self): 
        pass

    @staticmethod
    @contextmanager
    def create_temp_directory():
        try:
            # A normal directory is created here because tempfile.TemporaryDirectory()
            # creates a folder-like object, instead of a real directory and
            #  scandir cannot handle it
            # each test that needs a directory uses a uuid to create unique names
            # so that it does not interfere with directories of other tests
            folder_name = './temp_{}'.format(uuid1())
            if not exists('{}'.format(folder_name)):
                mkdir("{}".format(folder_name))

            yield folder_name
        finally:
            rmtree("./{}".format(folder_name))