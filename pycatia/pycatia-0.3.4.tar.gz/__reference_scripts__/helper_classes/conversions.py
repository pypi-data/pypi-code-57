type_conversion = {
    'boolean': 'bool',
    'long': 'int',
    'double': 'float',
    'float': 'float',
    'CATSafeArrayVariant': 'tuple',
    'CATBSTR': 'str',
    'CATBaseDispatch': 'AnyObject',
    'short': 'enum'
}


def convert_type(text):

    if text in type_conversion:
        return type_conversion[text]

    return text