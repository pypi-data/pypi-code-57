'''_874.py

CylindricalGearSetLoadDistributionAnalysis
'''


from typing import List

from mastapy.gears.rating.cylindrical import _397
from mastapy._internal import constructor, conversion
from mastapy.gears.ltca.cylindrical import _871
from mastapy.gears.ltca import _863
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalGearSetLoadDistributionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetLoadDistributionAnalysis',)


class CylindricalGearSetLoadDistributionAnalysis(_863.GearSetLoadDistributionAnalysis):
    '''CylindricalGearSetLoadDistributionAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def rating(self) -> '_397.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_397.CylindricalGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def meshes(self) -> 'List[_871.CylindricalGearMeshLoadDistributionAnalysis]':
        '''List[CylindricalGearMeshLoadDistributionAnalysis]: 'Meshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Meshes, constructor.new(_871.CylindricalGearMeshLoadDistributionAnalysis))
        return value
