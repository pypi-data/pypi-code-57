'''_1689.py

BearingProtectionDetailsModifier
'''


from mastapy.bearings.bearing_designs.rolling import _1690
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BEARING_PROTECTION_DETAILS_MODIFIER = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'BearingProtectionDetailsModifier')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingProtectionDetailsModifier',)


class BearingProtectionDetailsModifier(_1.APIBase):
    '''BearingProtectionDetailsModifier

    This is a mastapy class.
    '''

    TYPE = _BEARING_PROTECTION_DETAILS_MODIFIER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingProtectionDetailsModifier.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def protection_level(self) -> '_1690.BearingProtectionLevel':
        '''BearingProtectionLevel: 'ProtectionLevel' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ProtectionLevel)
        return constructor.new(_1690.BearingProtectionLevel)(value) if value else None

    @protection_level.setter
    def protection_level(self, value: '_1690.BearingProtectionLevel'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProtectionLevel = value

    @property
    def password_to_unprotect(self) -> 'str':
        '''str: 'PasswordToUnprotect' is the original name of this property.'''

        return self.wrapped.PasswordToUnprotect

    @password_to_unprotect.setter
    def password_to_unprotect(self, value: 'str'):
        self.wrapped.PasswordToUnprotect = str(value) if value else None

    @property
    def password_to_protect(self) -> 'str':
        '''str: 'PasswordToProtect' is the original name of this property.'''

        return self.wrapped.PasswordToProtect

    @password_to_protect.setter
    def password_to_protect(self, value: 'str'):
        self.wrapped.PasswordToProtect = str(value) if value else None

    @property
    def confirm_password_to_protect(self) -> 'str':
        '''str: 'ConfirmPasswordToProtect' is the original name of this property.'''

        return self.wrapped.ConfirmPasswordToProtect

    @confirm_password_to_protect.setter
    def confirm_password_to_protect(self, value: 'str'):
        self.wrapped.ConfirmPasswordToProtect = str(value) if value else None
