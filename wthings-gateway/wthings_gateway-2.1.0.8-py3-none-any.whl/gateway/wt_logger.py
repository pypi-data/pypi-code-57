import logging
import logging.handlers


class TBLoggerHandler(logging. Handler):
    def __init__(self, gateway):
        self.current_log_level = 'NOTSET'
        super().__init__(logging.getLevelName(self.current_log_level))
        self.setLevel(logging.getLevelName('DEBUG'))
        self.__gateway = gateway
        self.activated = False
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s] - %(module)s - %(lineno)d - %(message)s'))
        self.loggers = ['service',
                        'storage',
                        'extension',
                        'converter',
                        'connector',
                        'tb_connection'
                        ]
        for logger in self.loggers:
            log = logging.getLogger(logger)
            log.addHandler(self.__gateway.main_handler)
            log.debug("Added remote handler to log %s", logger)

    def activate(self, log_level=None):
        try:
            for logger in self.loggers:
                if log_level is not None and logging.getLevelName(log_level) is not None:
                    if logger == 'tb_connection' and log_level == 'DEBUG':
                        log = logging.getLogger(logger)
                        log.setLevel(logging.getLevelName('INFO'))
                    else:
                        log = logging.getLogger(logger)
                        self.current_log_level = log_level
                        log.setLevel(logging.getLevelName(log_level))
        except Exception as e:
            log = logging.getLogger('service')
            log.exception(e)
        self.activated = True

    def handle(self, record):
        if self.activated:
            record = self.formatter.format(record)
            self.__gateway.send_to_storage(self.__gateway.name, {"deviceName": self.__gateway.name, "telemetry": [{'LOGS': record}]})

    def deactivate(self):
        self.activated = False
