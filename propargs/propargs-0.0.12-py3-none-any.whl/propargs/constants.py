from collections import namedtuple

SWITCH = '-'

OS = "OS"

PROPS_DIR = 'props_dir'

UTYPE = "user_type"

# user types (DUMMY type is only for automated test)
TERMINAL = "terminal"
IPYTHON = "iPython"
IPYTHON_NB = "iPython Notebook"
WEB = "Web browser"
DUMMY = "dummy"

VALUE = "val"
QUESTION = "question"
ATYPE = "atype"
HIVAL = "hival"
LOWVAL = "lowval"

BOOL = 'BOOL'
INT = 'INT'
FLT = 'DBL'
STR = 'STR'
CMPLX = 'CMPLX'
type_dict = {BOOL: bool, INT: int, FLT: float, CMPLX: complex, STR: str}
type_for_none = {BOOL: False, INT: 0, FLT: 0.0, CMPLX: 0j, STR: ''}

AutoLoadProp = namedtuple('AutoLoadProp', 'prop_name, default')
ENV_AUTO_LOAD_PROPS = [AutoLoadProp(prop_name=UTYPE, default=TERMINAL)]
