from .support.config import Config
from .foundation.application import Application

__version__ = '0.1.0'

config = Config()
app = Application(config)
