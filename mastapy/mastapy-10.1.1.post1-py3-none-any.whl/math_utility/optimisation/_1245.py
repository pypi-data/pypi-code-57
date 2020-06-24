'''_1245.py

SpecifyOptimisationInputAs
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SPECIFY_OPTIMISATION_INPUT_AS = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'SpecifyOptimisationInputAs')


__docformat__ = 'restructuredtext en'
__all__ = ('SpecifyOptimisationInputAs',)


class SpecifyOptimisationInputAs(Enum):
    '''SpecifyOptimisationInputAs

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SPECIFY_OPTIMISATION_INPUT_AS
    __hash__ = None

    SYMMETRIC_DEVIATION_FROM_ORIGINAL_DESIGN_PERCENTAGE = 0
    ASYMMETRIC_DEVIATION_FROM_ORIGINAL_DESIGN_PERCENTAGE = 1
    SYMMETRIC_DEVIATION_FROM_ORIGINAL_DESIGN_ABSOLUTE = 2
    ASYMMETRIC_DEVIATION_FROM_ORIGINAL_DESIGN_ABSOLUTE = 3
    ABSOLUTE_RANGE = 4
