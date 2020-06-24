'''_477.py

CylindricalGearMicroPittingResults
'''


from typing import List

from mastapy.gears.rating.cylindrical import _489
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MICRO_PITTING_RESULTS = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearMicroPittingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMicroPittingResults',)


class CylindricalGearMicroPittingResults(_1.APIBase):
    '''CylindricalGearMicroPittingResults

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MICRO_PITTING_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMicroPittingResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def micro_pitting_results_row(self) -> 'List[_489.MicroPittingResultsRow]':
        '''List[MicroPittingResultsRow]: 'MicroPittingResultsRow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MicroPittingResultsRow, constructor.new(_489.MicroPittingResultsRow))
        return value
