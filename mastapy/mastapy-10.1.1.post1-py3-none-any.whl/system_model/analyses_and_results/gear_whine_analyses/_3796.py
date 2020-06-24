'''_3796.py

ComponentGearWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses import (
    _3915, _3913, _3917, _3918,
    _3921, _3922, _3935, _3928,
    _3912, _3926, _3868, _3860,
    _3862, _3867, _3869, _3872,
    _3878, _3879, _3866, _3874,
    _3876, _3936, _3950, _3938,
    _3972, _3955, _3942, _3964,
    _3966, _3968, _3856, _3944,
    _3945, _3970, _3971, _3959,
    _3961, _3952, _3923, _3924,
    _3929, _3930, _3933
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model import (
    _1912, _1910, _1916, _1919,
    _1921, _1924, _1932, _1908,
    _1929, _1926, _1927, _1933,
    _1934, _1938
)
from mastapy.system_model.part_model.shaft_model import _1942
from mastapy.system_model.part_model.couplings import (
    _1967, _2015, _2016, _2017,
    _2018, _2019, _2021, _2022,
    _2023, _2024, _2025
)
from mastapy.system_model.part_model.gears import (
    _1994, _1996, _1997, _1998,
    _2002, _2003, _2004, _2005,
    _2006, _2007, _2008, _2009,
    _2010, _2011, _2012, _2013,
    _2014
)
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3808
from mastapy._internal.python_net import python_net_import

_COMPONENT_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ComponentGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentGearWhineAnalysis',)


class ComponentGearWhineAnalysis(_3808.PartGearWhineAnalysis):
    '''ComponentGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def coupled_modal_analysis(self) -> '_3915.ComponentModalAnalysis':
        '''ComponentModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3915.ComponentModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_bolt_modal_analysis(self) -> '_3913.BoltModalAnalysis':
        '''BoltModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'BoltModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to BoltModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3913.BoltModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_datum_modal_analysis(self) -> '_3917.DatumModalAnalysis':
        '''DatumModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'DatumModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to DatumModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3917.DatumModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_external_cad_model_modal_analysis(self) -> '_3918.ExternalCADModelModalAnalysis':
        '''ExternalCADModelModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'ExternalCADModelModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to ExternalCADModelModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3918.ExternalCADModelModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_guide_dxf_model_modal_analysis(self) -> '_3921.GuideDxfModelModalAnalysis':
        '''GuideDxfModelModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'GuideDxfModelModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to GuideDxfModelModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3921.GuideDxfModelModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_imported_fe_component_modal_analysis(self) -> '_3922.ImportedFEComponentModalAnalysis':
        '''ImportedFEComponentModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'ImportedFEComponentModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to ImportedFEComponentModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3922.ImportedFEComponentModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_shaft_modal_analysis(self) -> '_3935.ShaftModalAnalysis':
        '''ShaftModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'ShaftModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to ShaftModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3935.ShaftModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_planet_carrier_modal_analysis(self) -> '_3928.PlanetCarrierModalAnalysis':
        '''PlanetCarrierModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'PlanetCarrierModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to PlanetCarrierModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3928.PlanetCarrierModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_bearing_modal_analysis(self) -> '_3912.BearingModalAnalysis':
        '''BearingModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'BearingModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to BearingModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3912.BearingModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_oil_seal_modal_analysis(self) -> '_3926.OilSealModalAnalysis':
        '''OilSealModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'OilSealModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to OilSealModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3926.OilSealModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_shaft_hub_connection_modal_analysis(self) -> '_3868.ShaftHubConnectionModalAnalysis':
        '''ShaftHubConnectionModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'ShaftHubConnectionModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to ShaftHubConnectionModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3868.ShaftHubConnectionModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_clutch_half_modal_analysis(self) -> '_3860.ClutchHalfModalAnalysis':
        '''ClutchHalfModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'ClutchHalfModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to ClutchHalfModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3860.ClutchHalfModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_concept_coupling_half_modal_analysis(self) -> '_3862.ConceptCouplingHalfModalAnalysis':
        '''ConceptCouplingHalfModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'ConceptCouplingHalfModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to ConceptCouplingHalfModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3862.ConceptCouplingHalfModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_pulley_modal_analysis(self) -> '_3867.PulleyModalAnalysis':
        '''PulleyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'PulleyModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to PulleyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3867.PulleyModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_rolling_ring_modal_analysis(self) -> '_3869.RollingRingModalAnalysis':
        '''RollingRingModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'RollingRingModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to RollingRingModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3869.RollingRingModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_spring_damper_half_modal_analysis(self) -> '_3872.SpringDamperHalfModalAnalysis':
        '''SpringDamperHalfModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'SpringDamperHalfModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to SpringDamperHalfModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3872.SpringDamperHalfModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_torque_converter_pump_modal_analysis(self) -> '_3878.TorqueConverterPumpModalAnalysis':
        '''TorqueConverterPumpModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'TorqueConverterPumpModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to TorqueConverterPumpModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3878.TorqueConverterPumpModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_torque_converter_turbine_modal_analysis(self) -> '_3879.TorqueConverterTurbineModalAnalysis':
        '''TorqueConverterTurbineModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'TorqueConverterTurbineModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to TorqueConverterTurbineModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3879.TorqueConverterTurbineModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_cvt_pulley_modal_analysis(self) -> '_3866.CVTPulleyModalAnalysis':
        '''CVTPulleyModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'CVTPulleyModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to CVTPulleyModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3866.CVTPulleyModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_synchroniser_half_modal_analysis(self) -> '_3874.SynchroniserHalfModalAnalysis':
        '''SynchroniserHalfModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'SynchroniserHalfModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to SynchroniserHalfModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3874.SynchroniserHalfModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_synchroniser_sleeve_modal_analysis(self) -> '_3876.SynchroniserSleeveModalAnalysis':
        '''SynchroniserSleeveModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'SynchroniserSleeveModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to SynchroniserSleeveModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3876.SynchroniserSleeveModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_concept_gear_modal_analysis(self) -> '_3936.ConceptGearModalAnalysis':
        '''ConceptGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'ConceptGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to ConceptGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3936.ConceptGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_cylindrical_gear_modal_analysis(self) -> '_3950.CylindricalGearModalAnalysis':
        '''CylindricalGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'CylindricalGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to CylindricalGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3950.CylindricalGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_face_gear_modal_analysis(self) -> '_3938.FaceGearModalAnalysis':
        '''FaceGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'FaceGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to FaceGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3938.FaceGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_worm_gear_modal_analysis(self) -> '_3972.WormGearModalAnalysis':
        '''WormGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'WormGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to WormGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3972.WormGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_hypoid_gear_modal_analysis(self) -> '_3955.HypoidGearModalAnalysis':
        '''HypoidGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'HypoidGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to HypoidGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3955.HypoidGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_bevel_differential_gear_modal_analysis(self) -> '_3942.BevelDifferentialGearModalAnalysis':
        '''BevelDifferentialGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'BevelDifferentialGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to BevelDifferentialGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3942.BevelDifferentialGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_spiral_bevel_gear_modal_analysis(self) -> '_3964.SpiralBevelGearModalAnalysis':
        '''SpiralBevelGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'SpiralBevelGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to SpiralBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3964.SpiralBevelGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_straight_bevel_diff_gear_modal_analysis(self) -> '_3966.StraightBevelDiffGearModalAnalysis':
        '''StraightBevelDiffGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'StraightBevelDiffGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to StraightBevelDiffGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3966.StraightBevelDiffGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_straight_bevel_gear_modal_analysis(self) -> '_3968.StraightBevelGearModalAnalysis':
        '''StraightBevelGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'StraightBevelGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to StraightBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3968.StraightBevelGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_zerol_bevel_gear_modal_analysis(self) -> '_3856.ZerolBevelGearModalAnalysis':
        '''ZerolBevelGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'ZerolBevelGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to ZerolBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3856.ZerolBevelGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_bevel_differential_planet_gear_modal_analysis(self) -> '_3944.BevelDifferentialPlanetGearModalAnalysis':
        '''BevelDifferentialPlanetGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'BevelDifferentialPlanetGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to BevelDifferentialPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3944.BevelDifferentialPlanetGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_bevel_differential_sun_gear_modal_analysis(self) -> '_3945.BevelDifferentialSunGearModalAnalysis':
        '''BevelDifferentialSunGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'BevelDifferentialSunGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to BevelDifferentialSunGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3945.BevelDifferentialSunGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_straight_bevel_planet_gear_modal_analysis(self) -> '_3970.StraightBevelPlanetGearModalAnalysis':
        '''StraightBevelPlanetGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'StraightBevelPlanetGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to StraightBevelPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3970.StraightBevelPlanetGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_straight_bevel_sun_gear_modal_analysis(self) -> '_3971.StraightBevelSunGearModalAnalysis':
        '''StraightBevelSunGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'StraightBevelSunGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to StraightBevelSunGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3971.StraightBevelSunGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis(self) -> '_3959.KlingelnbergCycloPalloidHypoidGearModalAnalysis':
        '''KlingelnbergCycloPalloidHypoidGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to KlingelnbergCycloPalloidHypoidGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3959.KlingelnbergCycloPalloidHypoidGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis(self) -> '_3961.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis':
        '''KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3961.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_cylindrical_planet_gear_modal_analysis(self) -> '_3952.CylindricalPlanetGearModalAnalysis':
        '''CylindricalPlanetGearModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'CylindricalPlanetGearModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to CylindricalPlanetGearModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3952.CylindricalPlanetGearModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_mass_disc_modal_analysis(self) -> '_3923.MassDiscModalAnalysis':
        '''MassDiscModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'MassDiscModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to MassDiscModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3923.MassDiscModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_measurement_component_modal_analysis(self) -> '_3924.MeasurementComponentModalAnalysis':
        '''MeasurementComponentModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'MeasurementComponentModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to MeasurementComponentModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3924.MeasurementComponentModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_point_load_modal_analysis(self) -> '_3929.PointLoadModalAnalysis':
        '''PointLoadModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'PointLoadModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to PointLoadModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3929.PointLoadModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_power_load_modal_analysis(self) -> '_3930.PowerLoadModalAnalysis':
        '''PowerLoadModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'PowerLoadModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to PowerLoadModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3930.PowerLoadModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def coupled_modal_analysis_of_type_unbalanced_mass_modal_analysis(self) -> '_3933.UnbalancedMassModalAnalysis':
        '''UnbalancedMassModalAnalysis: 'CoupledModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CoupledModalAnalysis.__class__.__qualname__ != 'UnbalancedMassModalAnalysis':
            raise CastException('Failed to cast coupled_modal_analysis to UnbalancedMassModalAnalysis. Expected: {}.'.format(self.wrapped.CoupledModalAnalysis.__class__.__qualname__))

        return constructor.new(_3933.UnbalancedMassModalAnalysis)(self.wrapped.CoupledModalAnalysis) if self.wrapped.CoupledModalAnalysis else None

    @property
    def component_design(self) -> '_1912.Component':
        '''Component: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1912.Component)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bolt(self) -> '_1910.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Bolt':
            raise CastException('Failed to cast component_design to Bolt. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1910.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_datum(self) -> '_1916.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Datum':
            raise CastException('Failed to cast component_design to Datum. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1916.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_external_cad_model(self) -> '_1919.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ExternalCADModel':
            raise CastException('Failed to cast component_design to ExternalCADModel. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1919.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_guide_dxf_model(self) -> '_1921.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'GuideDxfModel':
            raise CastException('Failed to cast component_design to GuideDxfModel. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1921.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_imported_fe_component(self) -> '_1924.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ImportedFEComponent':
            raise CastException('Failed to cast component_design to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1924.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Shaft':
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_planet_carrier(self) -> '_1932.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'PlanetCarrier':
            raise CastException('Failed to cast component_design to PlanetCarrier. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1932.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bearing(self) -> '_1908.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Bearing':
            raise CastException('Failed to cast component_design to Bearing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1908.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_oil_seal(self) -> '_1929.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'OilSeal':
            raise CastException('Failed to cast component_design to OilSeal. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1929.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft_hub_connection(self) -> '_1967.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ShaftHubConnection':
            raise CastException('Failed to cast component_design to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1967.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_mass_disc(self) -> '_1926.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'MassDisc':
            raise CastException('Failed to cast component_design to MassDisc. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1926.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_measurement_component(self) -> '_1927.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'MeasurementComponent':
            raise CastException('Failed to cast component_design to MeasurementComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1927.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_point_load(self) -> '_1933.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'PointLoad':
            raise CastException('Failed to cast component_design to PointLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1933.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_power_load(self) -> '_1934.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'PowerLoad':
            raise CastException('Failed to cast component_design to PowerLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1934.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_unbalanced_mass(self) -> '_1938.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'UnbalancedMass':
            raise CastException('Failed to cast component_design to UnbalancedMass. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1938.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear(self) -> '_1994.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ConceptGear':
            raise CastException('Failed to cast component_design to ConceptGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1994.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear(self) -> '_1996.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CylindricalGear':
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1996.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear(self) -> '_1997.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'FaceGear':
            raise CastException('Failed to cast component_design to FaceGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1997.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear(self) -> '_1998.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'WormGear':
            raise CastException('Failed to cast component_design to WormGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1998.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear(self) -> '_2002.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'HypoidGear':
            raise CastException('Failed to cast component_design to HypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2002.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear(self) -> '_2003.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialGear':
            raise CastException('Failed to cast component_design to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2003.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear(self) -> '_2004.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SpiralBevelGear':
            raise CastException('Failed to cast component_design to SpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2004.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear(self) -> '_2005.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelDiffGear':
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2005.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear(self) -> '_2006.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelGear':
            raise CastException('Failed to cast component_design to StraightBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2006.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear(self) -> '_2007.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ZerolBevelGear':
            raise CastException('Failed to cast component_design to ZerolBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2007.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_planet_gear(self) -> '_2008.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialPlanetGear':
            raise CastException('Failed to cast component_design to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2008.BevelDifferentialPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_sun_gear(self) -> '_2009.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialSunGear':
            raise CastException('Failed to cast component_design to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2009.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_planet_gear(self) -> '_2010.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelPlanetGear':
            raise CastException('Failed to cast component_design to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2010.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_sun_gear(self) -> '_2011.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelSunGear':
            raise CastException('Failed to cast component_design to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2011.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2012.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGear':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2012.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2013.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGear':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2013.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_planet_gear(self) -> '_2014.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CylindricalPlanetGear':
            raise CastException('Failed to cast component_design to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2014.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch_half(self) -> '_2015.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ClutchHalf':
            raise CastException('Failed to cast component_design to ClutchHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2015.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling_half(self) -> '_2016.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ConceptCouplingHalf':
            raise CastException('Failed to cast component_design to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2016.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_pulley(self) -> '_2017.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Pulley':
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2017.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring(self) -> '_2018.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'RollingRing':
            raise CastException('Failed to cast component_design to RollingRing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2018.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper_half(self) -> '_2019.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SpringDamperHalf':
            raise CastException('Failed to cast component_design to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2019.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_pump(self) -> '_2021.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'TorqueConverterPump':
            raise CastException('Failed to cast component_design to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2021.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_turbine(self) -> '_2022.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'TorqueConverterTurbine':
            raise CastException('Failed to cast component_design to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2022.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt_pulley(self) -> '_2023.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CVTPulley':
            raise CastException('Failed to cast component_design to CVTPulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2023.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_half(self) -> '_2024.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SynchroniserHalf':
            raise CastException('Failed to cast component_design to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2024.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_sleeve(self) -> '_2025.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SynchroniserSleeve':
            raise CastException('Failed to cast component_design to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2025.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
