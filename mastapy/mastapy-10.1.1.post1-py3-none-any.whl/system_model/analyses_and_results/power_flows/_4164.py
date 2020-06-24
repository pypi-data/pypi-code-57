'''_4164.py

CylindricalGearMeshPowerFlow
'''


from mastapy.system_model.connections_and_sockets.gears import _1798
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2244
from mastapy.gears.rating.cylindrical import _476
from mastapy.system_model.analyses_and_results.power_flows import _4173
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CylindricalGearMeshPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshPowerFlow',)


class CylindricalGearMeshPowerFlow(_4173.GearMeshPowerFlow):
    '''CylindricalGearMeshPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2244.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def rating(self) -> '_476.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_476.CylindricalGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_476.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_476.CylindricalGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
