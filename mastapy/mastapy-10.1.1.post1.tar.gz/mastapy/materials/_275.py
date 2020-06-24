'''_275.py

WindTurbineStandards
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_WIND_TURBINE_STANDARDS = python_net_import('SMT.MastaAPI.Materials', 'WindTurbineStandards')


__docformat__ = 'restructuredtext en'
__all__ = ('WindTurbineStandards',)


class WindTurbineStandards(Enum):
    '''WindTurbineStandards

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _WIND_TURBINE_STANDARDS
    __hash__ = None

    NONE = 0
    GL = 1
    ISO_814004 = 2
