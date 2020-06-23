# Copyright 2020 Cisco Systems, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
Main file that parses the arguments and sets up the REST handler.
'''

import argparse
import sys
from workload_auto import dcnm_top
from workload_auto import logger
from workload_auto import utils

class WlAuto:
    '''
    Main worlkoad automation class.
    '''
    def __init__(self):
        '''
        Init routine to parse the arguments and calls the top level Class
        apart from setting up the REST handler.
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--config", dest="config",
                            default='/etc/vmm_workload_auto/conf.yml',
                            help="Provide configuration file", metavar="FILE")
        args = parser.parse_args()
        if args.config is None:
            print("config file not present")
            return
        print("Config file is " + args.config)
        file_dict, exc = utils.yml_file_read(args.config)
        if not file_dict:
            print("Exception in config file read ", exc)
            return
        print("file content is ", file_dict)
        log_file = file_dict.get('LogFile', '/tmp/tmplog')
        logger.set_logging(log_file)
        dcnm_top.DcnmTop(file_dict)

def wl_auto_main():
    '''
    Main init routine.
    '''
    WlAuto()

if __name__ == '__main__':
    sys.exit(WlAuto())
