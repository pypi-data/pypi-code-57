# There shouldn't be an __init__.py in this dir,
# but we need it to shup up the flake8 logger

from logging import getLogger

getLogger('flake8').propagate = False
