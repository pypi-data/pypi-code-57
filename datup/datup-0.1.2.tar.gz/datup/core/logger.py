import logging
import uuid
import os

''' 
The Logger class must be instantiaded for write a log file.
This class must be called through Datup class
'''
class Logger:
    def __init__(
        self,
        suffix_name,
        local_path
    ):
        self.suffix_name = suffix_name
        self.local_path = local_path
        self.logger = logging.getLogger('__name__')
        self.logger.setLevel(logging.DEBUG)
        self.log_filename = self.suffix_name+str(uuid.uuid4())+'.log'
        self.file_handler = logging.FileHandler(os.path.join(self.local_path, self.log_filename))
        self.file_format = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.file_format)
        self.logger.addHandler(self.file_handler)