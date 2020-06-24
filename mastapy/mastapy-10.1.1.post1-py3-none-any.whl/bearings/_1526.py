'''_1526.py

RollingBearingKey
'''


from mastapy.utility.databases import _1339
from mastapy._internal.python_net import python_net_import

_ROLLING_BEARING_KEY = python_net_import('SMT.MastaAPI.Bearings', 'RollingBearingKey')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingBearingKey',)


class RollingBearingKey(_1339.DatabaseKey):
    '''RollingBearingKey

    This is a mastapy class.
    '''

    TYPE = _ROLLING_BEARING_KEY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingBearingKey.TYPE'):
        super().__init__(instance_to_wrap)
