'''_3714.py

CylindricalGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2328
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3713, _3663, _3717
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'CylindricalGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetDynamicAnalysis',)


class CylindricalGearSetDynamicAnalysis(_3717.GearSetDynamicAnalysis):
    '''CylindricalGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2328.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2328.CylindricalGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def cylindrical_gears_dynamic_analysis(self) -> 'List[_3713.CylindricalGearDynamicAnalysis]':
        '''List[CylindricalGearDynamicAnalysis]: 'CylindricalGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsDynamicAnalysis, constructor.new(_3713.CylindricalGearDynamicAnalysis))
        return value

    @property
    def cylindrical_meshes_dynamic_analysis(self) -> 'List[_3663.CylindricalGearMeshDynamicAnalysis]':
        '''List[CylindricalGearMeshDynamicAnalysis]: 'CylindricalMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesDynamicAnalysis, constructor.new(_3663.CylindricalGearMeshDynamicAnalysis))
        return value
