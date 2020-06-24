'''_5950.py

CylindricalGearMeshMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets.gears import _1798
from mastapy.system_model.analyses_and_results.static_loads import _2244
from mastapy.system_model.analyses_and_results.mbd_analyses import _5960
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'CylindricalGearMeshMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshMultiBodyDynamicsAnalysis',)


class CylindricalGearMeshMultiBodyDynamicsAnalysis(_5960.GearMeshMultiBodyDynamicsAnalysis):
    '''CylindricalGearMeshMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def contact_stress_gear_a_left_flank(self) -> 'float':
        '''float: 'ContactStressGearALeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactStressGearALeftFlank

    @property
    def contact_stress_gear_b_left_flank(self) -> 'float':
        '''float: 'ContactStressGearBLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactStressGearBLeftFlank

    @property
    def contact_stress_gear_a_right_flank(self) -> 'float':
        '''float: 'ContactStressGearARightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactStressGearARightFlank

    @property
    def contact_stress_gear_b_right_flank(self) -> 'float':
        '''float: 'ContactStressGearBRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactStressGearBRightFlank

    @property
    def tooth_root_stress_gear_a_left_flank(self) -> 'float':
        '''float: 'ToothRootStressGearALeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothRootStressGearALeftFlank

    @property
    def tooth_root_stress_gear_b_left_flank(self) -> 'float':
        '''float: 'ToothRootStressGearBLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothRootStressGearBLeftFlank

    @property
    def tooth_root_stress_gear_a_right_flank(self) -> 'float':
        '''float: 'ToothRootStressGearARightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothRootStressGearARightFlank

    @property
    def tooth_root_stress_gear_b_right_flank(self) -> 'float':
        '''float: 'ToothRootStressGearBRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothRootStressGearBRightFlank

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
    def planetaries(self) -> 'List[CylindricalGearMeshMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMeshMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshMultiBodyDynamicsAnalysis))
        return value
