"""
Defines lo99ing's global (default) formatter.
"""
import logging


FORMAT = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
formatter = logging.Formatter(FORMAT)
