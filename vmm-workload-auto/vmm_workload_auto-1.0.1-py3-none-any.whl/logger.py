# Copyright 2020 Cisco Systems, Inc.
# All Rights Reserved.
#
#

'''
Simple logger module.
'''

import logging
import logging.handlers as log_hdlr

LOG_FRMT = '%(asctime)s %(levelname)8s [%(name)s] %(message)s'
LOG_DATE_FRMT = '%Y-%m-%d %H:%M:%S'
# 5MB
MAX_LOG_SIZE = 5000000
LOG_BACKUP_CNT = 10

_logger_dict = {}

def get_logging(name):
    '''
    Function to get the logger object.
    '''
    if name in _logger_dict:
        return _logger_dict[name]
    logger = logging.getLogger(name)
    _logger_dict[name] = logger
    return logger

def set_logging(filename, level=None):
    '''
    Main set logger function.
    '''
    #logging.basicConfig(filename=filename)
    #, level=level, format='%(asctime)s %(message)s')
    if level is None:
        level = logging.INFO
    log_format = LOG_FRMT
    log_date_format = LOG_DATE_FRMT
    log_prnt_format = logging.Formatter(fmt=log_format, datefmt=log_date_format)
    logger = logging.getLogger(None)
    logger.setLevel(level)
    handler = log_hdlr.RotatingFileHandler(filename, maxBytes=MAX_LOG_SIZE,
                                           backupCount=LOG_BACKUP_CNT)
    handler.setFormatter(log_prnt_format)
    logger.addHandler(handler)
