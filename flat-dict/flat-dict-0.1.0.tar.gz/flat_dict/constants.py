from types import SimpleNamespace


VERSION_KEY = '__fd_version__'

PRIMITIVE_TYPE_ENCODING = {
    int: 'd',
    float: 'f',
    bool: 'b',
    str: 's'
}

PRIMITIVE_TYPE_ENCODER = {
    v: k for k, v in PRIMITIVE_TYPE_ENCODING.items()
}
PRIMITIVE_TYPE_ENCODER['b'] = lambda v: int(v)

PRIMITIVE_TYPE_DECODER = {
    v: k for k, v in PRIMITIVE_TYPE_ENCODING.items()
}
PRIMITIVE_TYPE_DECODER['b'] = lambda v: bool(int(v))

PRIMITIVE_TYPES = set(PRIMITIVE_TYPE_ENCODING.keys())
PRIMITIVE_ENCODINGS = set(PRIMITIVE_TYPE_ENCODING.values())

KEY_SEPARATOR = {
    '[': SimpleNamespace(open='[', close=']'),
    ']': SimpleNamespace(open='[', close=']'),
    '.': SimpleNamespace(open='', close='.'),
    '|': SimpleNamespace(open='', close='|'),
    '/': SimpleNamespace(open='', close='/'),
    '\\': SimpleNamespace(open='', close='\\')
}

SUPPORTED_VERSIONS = [
    '1.0'
]
