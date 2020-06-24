'''_461.py

VerificationOfContactPattern
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_VERIFICATION_OF_CONTACT_PATTERN = python_net_import('SMT.MastaAPI.Gears.Rating.Iso10300', 'VerificationOfContactPattern')


__docformat__ = 'restructuredtext en'
__all__ = ('VerificationOfContactPattern',)


class VerificationOfContactPattern(Enum):
    '''VerificationOfContactPattern

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _VERIFICATION_OF_CONTACT_PATTERN
    __hash__ = None

    FOR_EACH_GEAR_SET_IN_ITS_HOUSING_UNDER_FULL_LOAD = 0
    FOR_EACH_GEAR_SET_UNDER_LIGHT_TEST_LOAD = 1
    FOR_A_SAMPLE_GEAR_SET_AND_ESTIMATED_FOR_FULL_LOAD = 2
