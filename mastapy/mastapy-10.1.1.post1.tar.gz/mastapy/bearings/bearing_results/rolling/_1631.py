'''_1631.py

LoadedNeedleRollerBearingElement
'''


from mastapy.bearings.bearing_results.rolling import _1619
from mastapy._internal.python_net import python_net_import

_LOADED_NEEDLE_ROLLER_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedNeedleRollerBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedNeedleRollerBearingElement',)


class LoadedNeedleRollerBearingElement(_1619.LoadedCylindricalRollerBearingElement):
    '''LoadedNeedleRollerBearingElement

    This is a mastapy class.
    '''

    TYPE = _LOADED_NEEDLE_ROLLER_BEARING_ELEMENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedNeedleRollerBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
