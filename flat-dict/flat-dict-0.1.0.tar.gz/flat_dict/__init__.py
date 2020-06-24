from .flat_dict import encode, decode
from .exceptions import InvalidKeyError, FormatError

__version__ = '0.1.0'


"""

LIMITATIONS:

    - the input dictionary cannot contain the reserved key "__fd_version__"

"""