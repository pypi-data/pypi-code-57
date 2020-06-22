__version__ = '0.0.12'
__author__ = 'Mike Kroutikov'
__author_email__ = 'pgmmpk@gmail.com'


from .api import (
    Config,
    ls,
    register,
    push,
    pull,
    purge,
    dataset,
    create,
)

from .dataset import Dataset