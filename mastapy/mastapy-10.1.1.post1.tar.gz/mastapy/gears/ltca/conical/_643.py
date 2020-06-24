'''_643.py

ConicalMeshLoadDistributionAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.load_case.conical import _660
from mastapy.gears.manufacturing.bevel import _568
from mastapy.gears.ltca.conical import _642
from mastapy.gears.ltca import _616
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_LOAD_DISTRIBUTION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.LTCA.Conical', 'ConicalMeshLoadDistributionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshLoadDistributionAnalysis',)


class ConicalMeshLoadDistributionAnalysis(_616.GearMeshLoadDistributionAnalysis):
    '''ConicalMeshLoadDistributionAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_LOAD_DISTRIBUTION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshLoadDistributionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_roll_angles(self) -> 'int':
        '''int: 'NumberOfRollAngles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfRollAngles

    @property
    def pinion_mean_te(self) -> 'float':
        '''float: 'PinionMeanTE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionMeanTE

    @property
    def pinion_peak_to_peak_te(self) -> 'float':
        '''float: 'PinionPeakToPeakTE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionPeakToPeakTE

    @property
    def wheel_peak_to_peak_te(self) -> 'float':
        '''float: 'WheelPeakToPeakTE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelPeakToPeakTE

    @property
    def conical_mesh_load_case(self) -> '_660.ConicalMeshLoadCase':
        '''ConicalMeshLoadCase: 'ConicalMeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_660.ConicalMeshLoadCase)(self.wrapped.ConicalMeshLoadCase) if self.wrapped.ConicalMeshLoadCase else None

    @property
    def conical_mesh_manufacturing_analysis(self) -> '_568.ConicalMeshManufacturingAnalysis':
        '''ConicalMeshManufacturingAnalysis: 'ConicalMeshManufacturingAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_568.ConicalMeshManufacturingAnalysis)(self.wrapped.ConicalMeshManufacturingAnalysis) if self.wrapped.ConicalMeshManufacturingAnalysis else None

    @property
    def meshed_gears(self) -> 'List[_642.ConicalMeshedGearLoadDistributionAnalysis]':
        '''List[ConicalMeshedGearLoadDistributionAnalysis]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshedGears, constructor.new(_642.ConicalMeshedGearLoadDistributionAnalysis))
        return value
