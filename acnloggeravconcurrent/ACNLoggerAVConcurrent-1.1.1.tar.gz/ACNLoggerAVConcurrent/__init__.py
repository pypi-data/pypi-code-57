#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import re
from logging.handlers import TimedRotatingFileHandler
import uuid
import os
from cloghandler import ConcurrentRotatingFileHandler
class ACNLogger:

	def debug(self, session, message):
		try:
			self.logger.debug(("["+session+"]  ["+self._service_name+"]  [DEBUG]  "+message).encode('utf8'))
		except:
			try:
				self.logger.debug("["+session+"]  ["+self._service_name+"]  [DEBUG]  "+message)
			except:
				self.logger.debug(("["+session+"]  ["+self._service_name+"]  [DEBUG]  "+message).decode('utf8'))

	def info(self, session, message):
		try:
			self.logger.info(("["+session+"]  ["+self._service_name+"]  [INFO]  "+message).encode('utf8'))
		except:
			try:
				self.logger.info("["+session+"]  ["+self._service_name+"]  [INFO]  "+message)
			except:
				self.logger.info(("["+session+"]  ["+self._service_name+"]  [INFO]  "+message).decode('utf8'))

	def warning(self, session, message):
		try:
			self.logger.warning(("["+session+"]  ["+self._service_name+"]  [WARNING]  "+message).encode('utf8'))
		except:
			try:
				self.logger.warning("["+session+"]  ["+self._service_name+"]  [WARNING]  "+message)
			except:
				self.logger.warning(("["+session+"]  ["+self._service_name+"]  [WARNING]  "+message).decode('utf8'))

	def error(self, session, e):
		try:
			self.logger.error(("["+session+"]  ["+self._service_name+"]  [ERROR]  "+str(e.__class__.__name__)+"  "+str(e)).encode('utf8'))
		except:
			try:
				self.logger.error("["+session+"]  ["+self._service_name+"]  [ERROR]  "+str(e.__class__.__name__)+"  "+str(e))
			except:
				self.logger.error(("["+session+"]  ["+self._service_name+"]  [ERROR]  "+str(e.__class__.__name__)+"  "+str(e)).decode('utf8'))

	def critical(self, session, e):
		try:
			self.logger.critical(("["+session+"]  ["+self._service_name+"]  [CRITICAL]  "+str(e.__class__.__name__)+"  "+str(e)).encode('utf8'))
		except:
			try:
				self.logger.critical("["+session+"]  ["+self._service_name+"]  [CRITICAL]  "+str(e.__class__.__name__)+"  "+str(e))
			except:
				self.logger.critical(("["+session+"]  ["+self._service_name+"]  [CRITICAL]  "+str(e.__class__.__name__)+"  "+str(e)).decode('utf8'))

	def exception(self, session, e):
		try:
			self.logger.error(("["+session+"]  ["+self._service_name+"]  [ERROR]  "+str(e.__class__.__name__)+"  "+str(e)).encode('utf8'))
		except:
			try:
				self.logger.error("["+session+"]  ["+self._service_name+"]  [ERROR]  "+str(e.__class__.__name__)+"  "+str(e))
			except:
				self.logger.error(("["+session+"]  ["+self._service_name+"]  [ERROR]  "+str(e.__class__.__name__)+"  "+str(e)).decode('utf8'))



	def __init__(self,name,file,console_level,logfile_level):

		offset_s = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone###These 3 lines
		offset = offset_s / 60 / 60 * -1												#are to get
		timezone = ["", "+"][offset >= 0]+str(offset).zfill(2)+"00"						#the timezone

		acn_logger=logging.getLogger(name) # Creating the new logger
		acn_logger.propagate=False

		console_handler=logging.StreamHandler()

		if console_level == "info":
			console_handler.setLevel(logging.INFO)
			acn_logger.setLevel(logging.INFO) # Setting new logger level to INFO or above
		else:
			console_handler.setLevel(logging.DEBUG)
			acn_logger.setLevel(logging.DEBUG) # Setting new logger level to INFO or above

		file_handler = ConcurrentRotatingFileHandler(file, "a", 1024 * 1024, 600)
		
		if logfile_level == "info":
			file_handler.setLevel(logging.INFO)
		else:
			file_handler.setLevel(logging.DEBUG)

		acn_logger.addHandler(file_handler) #Adding file handler to the new logger
		acn_logger.addHandler(console_handler)

		formatter=logging.Formatter('[%(asctime)s'+timezone+']  %(message)s') #Creating a formatter

		file_handler.setFormatter(formatter) #Setting handler format
		console_handler.setFormatter(formatter)

		self.logger=acn_logger
		self._service_name=name

		self.info("UNDEFINED","STARTING MICROSERVICE")


def get_unique_logger(name, path,console_level="",logfile_level=""):
	unique_id = str(uuid.uuid4())
	logger_name = name + "_" + unique_id
	logger_path = os.path.join(path, logger_name + ".log")

	return ACNLogger(name=logger_name, file=logger_path,console_level=console_level,logfile_level=logfile_level)