'''_1497.py

RaceTolerance
'''


from mastapy.bearings.tolerances import _1498, _1493
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_RACE_TOLERANCE = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'RaceTolerance')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceTolerance',)


class RaceTolerance(_1493.InterferenceTolerance):
    '''RaceTolerance

    This is a mastapy class.
    '''

    TYPE = _RACE_TOLERANCE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RaceTolerance.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def roundness_specification(self) -> '_1498.RoundnessSpecification':
        '''RoundnessSpecification: 'RoundnessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1498.RoundnessSpecification)(self.wrapped.RoundnessSpecification) if self.wrapped.RoundnessSpecification else None
