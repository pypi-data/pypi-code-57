import pkgutil
res = pkgutil.get_data('spintop', 'VERSION')
__version__ = res.decode()

from .env import Spintop
