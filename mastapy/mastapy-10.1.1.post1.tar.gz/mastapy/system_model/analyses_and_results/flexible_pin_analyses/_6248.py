'''_6248.py

FlexiblePinAnalysisManufactureLevel
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4020
from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _6244
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ANALYSIS_MANUFACTURE_LEVEL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'FlexiblePinAnalysisManufactureLevel')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAnalysisManufactureLevel',)


class FlexiblePinAnalysisManufactureLevel(_6244.FlexiblePinAnalysis):
    '''FlexiblePinAnalysisManufactureLevel

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ANALYSIS_MANUFACTURE_LEVEL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAnalysisManufactureLevel.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def load_sharing_factors(self) -> 'List[float]':
        '''List[float]: 'LoadSharingFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadSharingFactors, float)
        return value

    @property
    def planetary_mesh_analysis(self) -> '_4020.CylindricalGearMeshParametricStudyTool':
        '''CylindricalGearMeshParametricStudyTool: 'PlanetaryMeshAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4020.CylindricalGearMeshParametricStudyTool)(self.wrapped.PlanetaryMeshAnalysis) if self.wrapped.PlanetaryMeshAnalysis else None
