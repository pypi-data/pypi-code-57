
from datetime import datetime

from .deaths import *

def cache_deaths():
    dt = datetime.now()
    deaths(output = True, cache = True)
    print(dt)

__all__ = ["cache_deaths"]