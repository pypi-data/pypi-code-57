'''_5012.py

CylindricalGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2065
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6095
from mastapy.system_model.analyses_and_results.mbd_analyses import _5011, _5010, _5023
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'CylindricalGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetMultiBodyDynamicsAnalysis',)


class CylindricalGearSetMultiBodyDynamicsAnalysis(_5023.GearSetMultiBodyDynamicsAnalysis):
    '''CylindricalGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2065.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2065.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6095.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6095.CylindricalGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5011.CylindricalGearMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5011.CylindricalGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_gears_multi_body_dynamics_analysis(self) -> 'List[_5011.CylindricalGearMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMultiBodyDynamicsAnalysis]: 'CylindricalGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsMultiBodyDynamicsAnalysis, constructor.new(_5011.CylindricalGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_meshes_multi_body_dynamics_analysis(self) -> 'List[_5010.CylindricalGearMeshMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMeshMultiBodyDynamicsAnalysis]: 'CylindricalMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesMultiBodyDynamicsAnalysis, constructor.new(_5010.CylindricalGearMeshMultiBodyDynamicsAnalysis))
        return value
