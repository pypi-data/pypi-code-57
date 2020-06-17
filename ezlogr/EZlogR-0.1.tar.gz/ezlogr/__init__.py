import json
import logging
import datetime

class Ezlogr(object):
    def __init__(self, filename=None, tags=None):
        """Thisis the main setup method for Ezlogr. Here we pull in the filename and tags, as well
        as setup the logger. The formatting here is minimal because we will be saving everything
        as JSON!
        """
        self.tags = tags
        self.filename = filename
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler(filename + ".log")
        self.handler.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)
    
    def create_timestamp(self, now):
        """This returns a string in the format:
        Hour as 0 padded decimal: 00...23
        Minute as 0 padded decimal: 00...59
        Second as 0 padded decimal: 00...59
        "."
        Microsecond as a decimal number, zero-padded on the left: 000000...999999
        """
        timestamp = now.strftime('%H%M%S.%f')
        return timestamp

    def create_datestamp(self, now):
        """This returns a string in the format:
        Day as 0 padded decimal: 01...31
        Month as 0 padded decimal: 01...12
        Year with century as decimal: 1970...2040
        """
        datestamp = now.strftime('%d%m%Y')
        return datestamp

    def create_human_readable_timestamp(self, now):
        """This returns a string in a human readable format for the system locale.
        """
        hrdatetime = now.strftime('%c')
        return hrdatetime

    def log_builder(self, log_level, hrtimestamp, datestamp, timestamp, log_msg, tags):
        """This returns a dict with several values set such as datestamp, 
        timestamp, log_msg, tags, etc.

        Note: This is a flexible dict that can change as grow as the product
        requires.
        """
        log_body = {}
        log_body["filename"] = self.filename
        log_body["log_level"] = log_level
        log_body["hrtimestamp"] = hrtimestamp
        log_body["datestamp"] = datestamp
        log_body["timestamp"] = timestamp
        log_body["log_msg"] = log_msg
        log_body["tags"] = tags
        return log_body

    def info(self, log_msg):
        """This is the basic info method for writing info level logs.
        """
        now = datetime.datetime.now()
        log_level = "info"
        datestamp = self.create_datestamp(now)
        timestamp = self.create_timestamp(now)
        hrtimestemp = self.create_human_readable_timestamp(now)
        tags = json.dumps(self.tags)
        log_body = self.log_builder(log_level, hrtimestemp, datestamp, timestamp, log_msg, tags)
        self.logger.info(log_body)

    def warn(self, log_msg, tags=None):
        """This is the warn method for writing warn level logs.
        """
        now = datetime.datetime.now()
        log_level = "warn"
        datestamp = self.create_datestamp(now)
        timestamp = self.create_timestamp(now)
        hrtimestemp = self.create_human_readable_timestamp(now)
        tags = json.dumps(self.tags)
        log_body = self.log_builder(log_level, hrtimestemp, datestamp, timestamp, log_msg, tags)
        self.logger.info(log_body)
      
    def critical(self, log_msg, tags=None):
        """This is the critical method for writing warn level logs.
        """
        now = datetime.datetime.now()
        log_level = "critical"
        datestamp = self.create_datestamp(now)
        timestamp = self.create_timestamp(now)
        hrtimestemp = self.create_human_readable_timestamp(now)
        tags = json.dumps(self.tags)
        log_body = self.log_builder(log_level, hrtimestemp, datestamp, timestamp, log_msg, tags)
        self.logger.info(log_body)
