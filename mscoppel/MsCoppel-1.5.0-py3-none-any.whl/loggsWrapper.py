import os
import socket
import time
import datetime
from fluent import asyncsender as sender

class LoggerWrapper(object):

    name = 'FLUENT_LOGS'

    __name = None
    __APP = ''
    __SERVICE = ''
    __VERSION = ''
    __BROKERS = ''
    __FRAMEWORK_VERSION = ''
    __HOSTNAME = ''
    __PRODUCTION = False

    __LEVELS = {
        'FATAL': 60,
        'ERROR': 50,
        'WARNING': 40,
        'INFO': 30,
        'DEBUG': 20,
        'TRACE': 10,
    }

    __logger = None

    def __init__(self, name):
        self.__name = name
        # Conexion con Fluentd
        self.__logger = sender.FluentSender(
            'coppelio.logs',
            host=os.environ.get('FLUENTD_HOST', 'localhost'),
            port=os.environ.get('FLUENTD_PORT', 24224),
            queue_circular=True
        )
        # Asignar el hostname
        self.__HOSTNAME = socket.gethostname()
        # Production
        self.__PRODUCTION = False if os.environ.get('PRODUCTION', None) is None else True

    def set_conf(self, app, service, version, brokers, frmversion):
        """
            Metodo para realizar la configuraciones extra del servicio
            para su procesamiento en Fluentd.
        """
        self.__APP = app
        self.__SERVICE = service
        self.__VERSION = version
        self.__BROKERS = brokers
        self.__FRAMEWORK_VERSION = frmversion

    def trace(self, message, data={}):
        self._log('TRACE', message, data)

    def debug(self, message, data={}):
        self._log('DEBUG', message, data)

    def info(self, message, data={}):
        self._log('INFO', message, data)

    def warn(self, message, data={}):
        self._log('WARNING', message, data)

    def warning(self, message, data={}):
        return self.warn(message, data)

    def fatal(self, message, data={}):
        self._log('FATAL', message, data)

    def error(self, message, data={}):
        self._log('ERROR', message, data)

    def log(self, level, message, data={}):
        self._log(level, message, data)

    def _log(self, level, message='', data={}):
        # Recuperar el level
        _level = self.__LEVELS.get(level, 10)
        # Logss
        log = {
            '@timestanp': datetime.datetime.now().isoformat(),
            'log_type': 'app',
            'level': _level,
            'type': level,
            'production': self.__PRODUCTION,
            'app': self.__APP,
            'service': self.__SERVICE,
            'version': self.__VERSION,
            'brokers': self.__BROKERS,
            'framework_version': self.__FRAMEWORK_VERSION,
            'hostname': self.__HOSTNAME,
            'message': message,
            'data': data,
        }
        # Publicar el log
        self.__logger.emit_with_time('app', int(time.time()), log)
