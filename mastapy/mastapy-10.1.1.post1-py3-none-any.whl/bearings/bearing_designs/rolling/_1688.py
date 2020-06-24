'''_1688.py

BearingProtection
'''


from mastapy.bearings.bearing_designs.rolling import _1690
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BEARING_PROTECTION = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'BearingProtection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingProtection',)


class BearingProtection(_1.APIBase):
    '''BearingProtection

    This is a mastapy class.
    '''

    TYPE = _BEARING_PROTECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingProtection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def protection_level(self) -> '_1690.BearingProtectionLevel':
        '''BearingProtectionLevel: 'ProtectionLevel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ProtectionLevel)
        return constructor.new(_1690.BearingProtectionLevel)(value) if value else None

    @property
    def bearing_is_protected(self) -> 'bool':
        '''bool: 'BearingIsProtected' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BearingIsProtected

    @property
    def internal_geometry_hidden(self) -> 'str':
        '''str: 'InternalGeometryHidden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InternalGeometryHidden

    @property
    def advanced_bearing_results_hidden(self) -> 'str':
        '''str: 'AdvancedBearingResultsHidden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AdvancedBearingResultsHidden
