'''_1210.py

TighteningTechniques
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_TIGHTENING_TECHNIQUES = python_net_import('SMT.MastaAPI.Bolts', 'TighteningTechniques')


__docformat__ = 'restructuredtext en'
__all__ = ('TighteningTechniques',)


class TighteningTechniques(Enum):
    '''TighteningTechniques

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _TIGHTENING_TECHNIQUES
    __hash__ = None

    ULTRASOUND_ELONGATION_CONTROLLED_TIGHTENING = 0
    MECHANICAL_ELONGATION_CONTROLLED_TIGHTENING = 1
    YIELD_CONTROLLED_TIGHTENING = 2
    ANGLE_CONTROLLED_TIGHTENING = 3
    HYDRAULIC_TIGHTENING = 4
    TORQUE_WRENCH_WITH_TIGHTENING_TORQUE_EXPERIMENTALLY_DETERMINED = 5
    TORQUE_WRENCH_WITH_ESTIMATED_FRICTION_COEFFICIENT_OF_CLASS_B = 6
    TORQUE_WRENCH_WITH_ESTIMATED_FRICTION_COEFFICIENT_OF_CLASS_A = 7
    IMPACT_WRENCH_TIGHTENING = 8
