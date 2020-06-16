# Copyright 2020 Cisco Systems, Inc.
# All Rights Reserved.
#
#

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
