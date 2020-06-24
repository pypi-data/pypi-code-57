'''_4658.py

AssemblySteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _1904
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2277
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _4659, _4661, _4663, _4671,
    _4670, _4674, _4679, _4681,
    _4693, _4695, _4702, _4704,
    _4710, _4712, _4718, _4721,
    _4723, _4724, _4726, _4730,
    _4731, _4732, _4738, _4734,
    _4739, _4743, _4747, _4751,
    _4754, _4761, _4764, _4766,
    _4769, _4772, _4653
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'AssemblySteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySteadyStateSynchronousResponse',)


class AssemblySteadyStateSynchronousResponse(_4653.AbstractAssemblySteadyStateSynchronousResponse):
    '''AssemblySteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblySteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1904.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1904.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2277.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2277.AssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_4659.BearingSteadyStateSynchronousResponse]':
        '''List[BearingSteadyStateSynchronousResponse]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4659.BearingSteadyStateSynchronousResponse))
        return value

    @property
    def belt_drives(self) -> 'List[_4661.BeltDriveSteadyStateSynchronousResponse]':
        '''List[BeltDriveSteadyStateSynchronousResponse]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4661.BeltDriveSteadyStateSynchronousResponse))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4663.BevelDifferentialGearSetSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSetSteadyStateSynchronousResponse]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4663.BevelDifferentialGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def bolts(self) -> 'List[_4671.BoltSteadyStateSynchronousResponse]':
        '''List[BoltSteadyStateSynchronousResponse]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4671.BoltSteadyStateSynchronousResponse))
        return value

    @property
    def bolted_joints(self) -> 'List[_4670.BoltedJointSteadyStateSynchronousResponse]':
        '''List[BoltedJointSteadyStateSynchronousResponse]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4670.BoltedJointSteadyStateSynchronousResponse))
        return value

    @property
    def clutches(self) -> 'List[_4674.ClutchSteadyStateSynchronousResponse]':
        '''List[ClutchSteadyStateSynchronousResponse]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4674.ClutchSteadyStateSynchronousResponse))
        return value

    @property
    def concept_couplings(self) -> 'List[_4679.ConceptCouplingSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingSteadyStateSynchronousResponse]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4679.ConceptCouplingSteadyStateSynchronousResponse))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4681.ConceptGearSetSteadyStateSynchronousResponse]':
        '''List[ConceptGearSetSteadyStateSynchronousResponse]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4681.ConceptGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def cv_ts(self) -> 'List[_4693.CVTSteadyStateSynchronousResponse]':
        '''List[CVTSteadyStateSynchronousResponse]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4693.CVTSteadyStateSynchronousResponse))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4695.CylindricalGearSetSteadyStateSynchronousResponse]':
        '''List[CylindricalGearSetSteadyStateSynchronousResponse]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4695.CylindricalGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4702.FaceGearSetSteadyStateSynchronousResponse]':
        '''List[FaceGearSetSteadyStateSynchronousResponse]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4702.FaceGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4704.FlexiblePinAssemblySteadyStateSynchronousResponse]':
        '''List[FlexiblePinAssemblySteadyStateSynchronousResponse]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4704.FlexiblePinAssemblySteadyStateSynchronousResponse))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4710.HypoidGearSetSteadyStateSynchronousResponse]':
        '''List[HypoidGearSetSteadyStateSynchronousResponse]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4710.HypoidGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4712.ImportedFEComponentSteadyStateSynchronousResponse]':
        '''List[ImportedFEComponentSteadyStateSynchronousResponse]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4712.ImportedFEComponentSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4718.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4718.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4721.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4721.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def mass_discs(self) -> 'List[_4723.MassDiscSteadyStateSynchronousResponse]':
        '''List[MassDiscSteadyStateSynchronousResponse]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4723.MassDiscSteadyStateSynchronousResponse))
        return value

    @property
    def measurement_components(self) -> 'List[_4724.MeasurementComponentSteadyStateSynchronousResponse]':
        '''List[MeasurementComponentSteadyStateSynchronousResponse]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4724.MeasurementComponentSteadyStateSynchronousResponse))
        return value

    @property
    def oil_seals(self) -> 'List[_4726.OilSealSteadyStateSynchronousResponse]':
        '''List[OilSealSteadyStateSynchronousResponse]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4726.OilSealSteadyStateSynchronousResponse))
        return value

    @property
    def planet_carriers(self) -> 'List[_4730.PlanetCarrierSteadyStateSynchronousResponse]':
        '''List[PlanetCarrierSteadyStateSynchronousResponse]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4730.PlanetCarrierSteadyStateSynchronousResponse))
        return value

    @property
    def point_loads(self) -> 'List[_4731.PointLoadSteadyStateSynchronousResponse]':
        '''List[PointLoadSteadyStateSynchronousResponse]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4731.PointLoadSteadyStateSynchronousResponse))
        return value

    @property
    def power_loads(self) -> 'List[_4732.PowerLoadSteadyStateSynchronousResponse]':
        '''List[PowerLoadSteadyStateSynchronousResponse]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4732.PowerLoadSteadyStateSynchronousResponse))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4738.ShaftHubConnectionSteadyStateSynchronousResponse]':
        '''List[ShaftHubConnectionSteadyStateSynchronousResponse]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4738.ShaftHubConnectionSteadyStateSynchronousResponse))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4734.RollingRingAssemblySteadyStateSynchronousResponse]':
        '''List[RollingRingAssemblySteadyStateSynchronousResponse]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4734.RollingRingAssemblySteadyStateSynchronousResponse))
        return value

    @property
    def shafts(self) -> 'List[_4739.ShaftSteadyStateSynchronousResponse]':
        '''List[ShaftSteadyStateSynchronousResponse]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4739.ShaftSteadyStateSynchronousResponse))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4743.SpiralBevelGearSetSteadyStateSynchronousResponse]':
        '''List[SpiralBevelGearSetSteadyStateSynchronousResponse]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4743.SpiralBevelGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def spring_dampers(self) -> 'List[_4747.SpringDamperSteadyStateSynchronousResponse]':
        '''List[SpringDamperSteadyStateSynchronousResponse]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4747.SpringDamperSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4751.StraightBevelDiffGearSetSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponse]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4751.StraightBevelDiffGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4754.StraightBevelGearSetSteadyStateSynchronousResponse]':
        '''List[StraightBevelGearSetSteadyStateSynchronousResponse]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4754.StraightBevelGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def synchronisers(self) -> 'List[_4761.SynchroniserSteadyStateSynchronousResponse]':
        '''List[SynchroniserSteadyStateSynchronousResponse]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4761.SynchroniserSteadyStateSynchronousResponse))
        return value

    @property
    def torque_converters(self) -> 'List[_4764.TorqueConverterSteadyStateSynchronousResponse]':
        '''List[TorqueConverterSteadyStateSynchronousResponse]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4764.TorqueConverterSteadyStateSynchronousResponse))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4766.UnbalancedMassSteadyStateSynchronousResponse]':
        '''List[UnbalancedMassSteadyStateSynchronousResponse]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4766.UnbalancedMassSteadyStateSynchronousResponse))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4769.WormGearSetSteadyStateSynchronousResponse]':
        '''List[WormGearSetSteadyStateSynchronousResponse]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4769.WormGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4772.ZerolBevelGearSetSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponse]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4772.ZerolBevelGearSetSteadyStateSynchronousResponse))
        return value
