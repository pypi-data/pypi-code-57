'''_2274.py

ImportedFEComponentSystemDeflection
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2001
from mastapy.system_model.analyses_and_results.static_loads import _6136
from mastapy.system_model.analyses_and_results.power_flows import _3275
from mastapy.nodal_analysis.component_mode_synthesis import _1496
from mastapy.nodal_analysis import _1384
from mastapy.math_utility.measured_vectors import _1118, _1113
from mastapy.system_model.analyses_and_results.system_deflections import _2208
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ImportedFEComponentSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentSystemDeflection',)


class ImportedFEComponentSystemDeflection(_2208.AbstractShaftOrHousingSystemDeflection):
    '''ImportedFEComponentSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def export_displacements(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ExportDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportDisplacements

    @property
    def export_forces(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ExportForces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExportForces

    @property
    def component_design(self) -> '_2001.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2001.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6136.ImportedFEComponentLoadCase':
        '''ImportedFEComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6136.ImportedFEComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3275.ImportedFEComponentPowerFlow':
        '''ImportedFEComponentPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3275.ImportedFEComponentPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def full_fe_results(self) -> '_1496.StaticCMSResults':
        '''StaticCMSResults: 'FullFEResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1496.StaticCMSResults)(self.wrapped.FullFEResults) if self.wrapped.FullFEResults else None

    @property
    def stiffness_in_world_coordinate_system_mn_rad(self) -> '_1384.NodalMatrix':
        '''NodalMatrix: 'StiffnessInWorldCoordinateSystemMNRad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1384.NodalMatrix)(self.wrapped.StiffnessInWorldCoordinateSystemMNRad) if self.wrapped.StiffnessInWorldCoordinateSystemMNRad else None

    @property
    def mass_in_world_coordinate_system_mn_rad_s_kg(self) -> '_1384.NodalMatrix':
        '''NodalMatrix: 'MassInWorldCoordinateSystemMNRadSKg' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1384.NodalMatrix)(self.wrapped.MassInWorldCoordinateSystemMNRadSKg) if self.wrapped.MassInWorldCoordinateSystemMNRadSKg else None

    @property
    def planetaries(self) -> 'List[ImportedFEComponentSystemDeflection]':
        '''List[ImportedFEComponentSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentSystemDeflection))
        return value

    @property
    def applied_internal_forces_in_world_coordinate_system(self) -> 'List[_1118.VectorWithLinearAndAngularComponents]':
        '''List[VectorWithLinearAndAngularComponents]: 'AppliedInternalForcesInWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AppliedInternalForcesInWorldCoordinateSystem, constructor.new(_1118.VectorWithLinearAndAngularComponents))
        return value

    @property
    def node_results_in_shaft_coordinate_system(self) -> 'List[_1113.ForceAndDisplacementResults]':
        '''List[ForceAndDisplacementResults]: 'NodeResultsInShaftCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.NodeResultsInShaftCoordinateSystem, constructor.new(_1113.ForceAndDisplacementResults))
        return value
