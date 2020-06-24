import logging
import os

DEFAULT_LEVEL = logging.DEBUG

class LoggingClient(logging.Logger):
    def __init__(self, config):
        # TODO:  Can I strongly type the config data structure?

        # Error checking
        assert config
        assert 'name' in config

        # Default or custom logging level
        level=config['level'] if 'level' in config else DEFAULT_LEVEL

        super().__init__(name=config['name'], level=level)

        # Console stream handler
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # add the handlers to the logger
        self.addHandler(ch)