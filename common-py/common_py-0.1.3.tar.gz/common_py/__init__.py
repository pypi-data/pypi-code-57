from pkgutil import extend_path

from .dict_extension import *
from .enum_argparse import *
from .file import *
from .folder import *
from .list_extension import *

__path__ = extend_path(__path__, "functional")

__version__ = "0.1.3"
