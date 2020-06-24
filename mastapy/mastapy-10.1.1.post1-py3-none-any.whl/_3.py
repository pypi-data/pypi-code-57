'''_3.py

MastaSettings
'''


from mastapy.bearings.bearing_results.rolling import _1593
from mastapy._internal import constructor
from mastapy.bearings import _1513, _1525
from mastapy.bolts import _1038, _1040, _1045
from mastapy.gears import _118, _119, _145
from mastapy.gears.gear_designs.cylindrical import (
    _774, _778, _779, _780
)
from mastapy.gears.gear_designs import _710, _716
from mastapy.gears.gear_set_pareto_optimiser import (
    _688, _689, _692, _693,
    _695, _696, _698, _699,
    _701, _702, _703, _704
)
from mastapy.gears.ltca.cylindrical import _628
from mastapy.gears.manufacturing.bevel import _584
from mastapy.gears.manufacturing.cylindrical.cutters import (
    _507, _513, _518, _519
)
from mastapy.gears.manufacturing.cylindrical import _399, _410
from mastapy.gears.materials import (
    _370, _372, _373, _374,
    _377, _380, _383, _384,
    _391
)
from mastapy.gears.rating.cylindrical import _261, _268
from mastapy.materials import (
    _53, _54, _75, _78
)
from mastapy.nodal_analysis import _1359, _1374
from mastapy.shafts import _25, _37
from mastapy.system_model.analyses_and_results.static_loads import _6102
from mastapy.system_model.optimization import _1815, _1824
from mastapy.system_model.part_model.gears.supercharger_rotor_set import _2103
from mastapy.system_model.part_model import _2011
from mastapy.utility.cad_export import _1345
from mastapy.utility.databases import _1340
from mastapy.utility import _1141, _1142
from mastapy.utility.scripting import _1264
from mastapy.utility.units_and_measurements import _1151
from mastapy._internal.python_net import python_net_import

_MASTA_SETTINGS = python_net_import('SMT.MastaAPI', 'MastaSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('MastaSettings',)


class MastaSettings:
    '''MastaSettings

    This is a mastapy class.
    '''

    TYPE = _MASTA_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MastaSettings.TYPE'):
        self.wrapped = instance_to_wrap

    @property
    def iso14179_settings_database(self) -> '_1593.ISO14179SettingsDatabase':
        '''ISO14179SettingsDatabase: 'ISO14179SettingsDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1593.ISO14179SettingsDatabase)(self.wrapped.ISO14179SettingsDatabase) if self.wrapped.ISO14179SettingsDatabase else None

    @property
    def bearing_settings(self) -> '_1513.BearingSettings':
        '''BearingSettings: 'BearingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1513.BearingSettings)(self.wrapped.BearingSettings) if self.wrapped.BearingSettings else None

    @property
    def rolling_bearing_database(self) -> '_1525.RollingBearingDatabase':
        '''RollingBearingDatabase: 'RollingBearingDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1525.RollingBearingDatabase)(self.wrapped.RollingBearingDatabase) if self.wrapped.RollingBearingDatabase else None

    @property
    def bolt_geometry_database(self) -> '_1038.BoltGeometryDatabase':
        '''BoltGeometryDatabase: 'BoltGeometryDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1038.BoltGeometryDatabase)(self.wrapped.BoltGeometryDatabase) if self.wrapped.BoltGeometryDatabase else None

    @property
    def bolt_material_database(self) -> '_1040.BoltMaterialDatabase':
        '''BoltMaterialDatabase: 'BoltMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1040.BoltMaterialDatabase)(self.wrapped.BoltMaterialDatabase) if self.wrapped.BoltMaterialDatabase else None

    @property
    def clamped_section_material_database(self) -> '_1045.ClampedSectionMaterialDatabase':
        '''ClampedSectionMaterialDatabase: 'ClampedSectionMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1045.ClampedSectionMaterialDatabase)(self.wrapped.ClampedSectionMaterialDatabase) if self.wrapped.ClampedSectionMaterialDatabase else None

    @property
    def bevel_hypoid_gear_design_settings(self) -> '_118.BevelHypoidGearDesignSettings':
        '''BevelHypoidGearDesignSettings: 'BevelHypoidGearDesignSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_118.BevelHypoidGearDesignSettings)(self.wrapped.BevelHypoidGearDesignSettings) if self.wrapped.BevelHypoidGearDesignSettings else None

    @property
    def bevel_hypoid_gear_rating_settings(self) -> '_119.BevelHypoidGearRatingSettings':
        '''BevelHypoidGearRatingSettings: 'BevelHypoidGearRatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_119.BevelHypoidGearRatingSettings)(self.wrapped.BevelHypoidGearRatingSettings) if self.wrapped.BevelHypoidGearRatingSettings else None

    @property
    def cylindrical_gear_defaults(self) -> '_774.CylindricalGearDefaults':
        '''CylindricalGearDefaults: 'CylindricalGearDefaults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_774.CylindricalGearDefaults)(self.wrapped.CylindricalGearDefaults) if self.wrapped.CylindricalGearDefaults else None

    @property
    def cylindrical_gear_design_constraints_database(self) -> '_778.CylindricalGearDesignConstraintsDatabase':
        '''CylindricalGearDesignConstraintsDatabase: 'CylindricalGearDesignConstraintsDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_778.CylindricalGearDesignConstraintsDatabase)(self.wrapped.CylindricalGearDesignConstraintsDatabase) if self.wrapped.CylindricalGearDesignConstraintsDatabase else None

    @property
    def cylindrical_gear_design_constraint_settings(self) -> '_779.CylindricalGearDesignConstraintSettings':
        '''CylindricalGearDesignConstraintSettings: 'CylindricalGearDesignConstraintSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_779.CylindricalGearDesignConstraintSettings)(self.wrapped.CylindricalGearDesignConstraintSettings) if self.wrapped.CylindricalGearDesignConstraintSettings else None

    @property
    def cylindrical_gear_design_settings(self) -> '_780.CylindricalGearDesignSettings':
        '''CylindricalGearDesignSettings: 'CylindricalGearDesignSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_780.CylindricalGearDesignSettings)(self.wrapped.CylindricalGearDesignSettings) if self.wrapped.CylindricalGearDesignSettings else None

    @property
    def design_constraint_collection_database(self) -> '_710.DesignConstraintCollectionDatabase':
        '''DesignConstraintCollectionDatabase: 'DesignConstraintCollectionDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_710.DesignConstraintCollectionDatabase)(self.wrapped.DesignConstraintCollectionDatabase) if self.wrapped.DesignConstraintCollectionDatabase else None

    @property
    def selected_design_constraints_collection(self) -> '_716.SelectedDesignConstraintsCollection':
        '''SelectedDesignConstraintsCollection: 'SelectedDesignConstraintsCollection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_716.SelectedDesignConstraintsCollection)(self.wrapped.SelectedDesignConstraintsCollection) if self.wrapped.SelectedDesignConstraintsCollection else None

    @property
    def micro_geometry_gear_set_design_space_search_strategy_database(self) -> '_688.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase':
        '''MicroGeometryGearSetDesignSpaceSearchStrategyDatabase: 'MicroGeometryGearSetDesignSpaceSearchStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_688.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase)(self.wrapped.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase) if self.wrapped.MicroGeometryGearSetDesignSpaceSearchStrategyDatabase else None

    @property
    def micro_geometry_gear_set_duty_cycle_design_space_search_strategy_database(self) -> '_689.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase':
        '''MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase: 'MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_689.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase)(self.wrapped.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase) if self.wrapped.MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase else None

    @property
    def pareto_cylindrical_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_692.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_692.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoCylindricalGearSetDutyCycleOptimisationStrategyDatabase else None

    @property
    def pareto_cylindrical_gear_set_optimisation_strategy_database(self) -> '_693.ParetoCylindricalGearSetOptimisationStrategyDatabase':
        '''ParetoCylindricalGearSetOptimisationStrategyDatabase: 'ParetoCylindricalGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_693.ParetoCylindricalGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoCylindricalGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoCylindricalGearSetOptimisationStrategyDatabase else None

    @property
    def pareto_face_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_695.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_695.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoFaceGearSetDutyCycleOptimisationStrategyDatabase else None

    @property
    def pareto_face_gear_set_optimisation_strategy_database(self) -> '_696.ParetoFaceGearSetOptimisationStrategyDatabase':
        '''ParetoFaceGearSetOptimisationStrategyDatabase: 'ParetoFaceGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_696.ParetoFaceGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoFaceGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoFaceGearSetOptimisationStrategyDatabase else None

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_698.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_698.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase else None

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(self) -> '_699.ParetoHypoidGearSetOptimisationStrategyDatabase':
        '''ParetoHypoidGearSetOptimisationStrategyDatabase: 'ParetoHypoidGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_699.ParetoHypoidGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoHypoidGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoHypoidGearSetOptimisationStrategyDatabase else None

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_701.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_701.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase else None

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(self) -> '_702.ParetoSpiralBevelGearSetOptimisationStrategyDatabase':
        '''ParetoSpiralBevelGearSetOptimisationStrategyDatabase: 'ParetoSpiralBevelGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_702.ParetoSpiralBevelGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoSpiralBevelGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoSpiralBevelGearSetOptimisationStrategyDatabase else None

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(self) -> '_703.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase':
        '''ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase: 'ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_703.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase)(self.wrapped.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase) if self.wrapped.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase else None

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(self) -> '_704.ParetoStraightBevelGearSetOptimisationStrategyDatabase':
        '''ParetoStraightBevelGearSetOptimisationStrategyDatabase: 'ParetoStraightBevelGearSetOptimisationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_704.ParetoStraightBevelGearSetOptimisationStrategyDatabase)(self.wrapped.ParetoStraightBevelGearSetOptimisationStrategyDatabase) if self.wrapped.ParetoStraightBevelGearSetOptimisationStrategyDatabase else None

    @property
    def cylindrical_gear_fe_settings(self) -> '_628.CylindricalGearFESettings':
        '''CylindricalGearFESettings: 'CylindricalGearFESettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_628.CylindricalGearFESettings)(self.wrapped.CylindricalGearFESettings) if self.wrapped.CylindricalGearFESettings else None

    @property
    def manufacturing_machine_database(self) -> '_584.ManufacturingMachineDatabase':
        '''ManufacturingMachineDatabase: 'ManufacturingMachineDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_584.ManufacturingMachineDatabase)(self.wrapped.ManufacturingMachineDatabase) if self.wrapped.ManufacturingMachineDatabase else None

    @property
    def cylindrical_formed_wheel_grinder_database(self) -> '_507.CylindricalFormedWheelGrinderDatabase':
        '''CylindricalFormedWheelGrinderDatabase: 'CylindricalFormedWheelGrinderDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_507.CylindricalFormedWheelGrinderDatabase)(self.wrapped.CylindricalFormedWheelGrinderDatabase) if self.wrapped.CylindricalFormedWheelGrinderDatabase else None

    @property
    def cylindrical_gear_plunge_shaver_database(self) -> '_513.CylindricalGearPlungeShaverDatabase':
        '''CylindricalGearPlungeShaverDatabase: 'CylindricalGearPlungeShaverDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_513.CylindricalGearPlungeShaverDatabase)(self.wrapped.CylindricalGearPlungeShaverDatabase) if self.wrapped.CylindricalGearPlungeShaverDatabase else None

    @property
    def cylindrical_gear_shaver_database(self) -> '_518.CylindricalGearShaverDatabase':
        '''CylindricalGearShaverDatabase: 'CylindricalGearShaverDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_518.CylindricalGearShaverDatabase)(self.wrapped.CylindricalGearShaverDatabase) if self.wrapped.CylindricalGearShaverDatabase else None

    @property
    def cylindrical_worm_grinder_database(self) -> '_519.CylindricalWormGrinderDatabase':
        '''CylindricalWormGrinderDatabase: 'CylindricalWormGrinderDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_519.CylindricalWormGrinderDatabase)(self.wrapped.CylindricalWormGrinderDatabase) if self.wrapped.CylindricalWormGrinderDatabase else None

    @property
    def cylindrical_hob_database(self) -> '_399.CylindricalHobDatabase':
        '''CylindricalHobDatabase: 'CylindricalHobDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_399.CylindricalHobDatabase)(self.wrapped.CylindricalHobDatabase) if self.wrapped.CylindricalHobDatabase else None

    @property
    def cylindrical_shaper_database(self) -> '_410.CylindricalShaperDatabase':
        '''CylindricalShaperDatabase: 'CylindricalShaperDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_410.CylindricalShaperDatabase)(self.wrapped.CylindricalShaperDatabase) if self.wrapped.CylindricalShaperDatabase else None

    @property
    def bevel_gear_iso_material_database(self) -> '_370.BevelGearIsoMaterialDatabase':
        '''BevelGearIsoMaterialDatabase: 'BevelGearIsoMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_370.BevelGearIsoMaterialDatabase)(self.wrapped.BevelGearIsoMaterialDatabase) if self.wrapped.BevelGearIsoMaterialDatabase else None

    @property
    def bevel_gear_material_database(self) -> '_372.BevelGearMaterialDatabase':
        '''BevelGearMaterialDatabase: 'BevelGearMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_372.BevelGearMaterialDatabase)(self.wrapped.BevelGearMaterialDatabase) if self.wrapped.BevelGearMaterialDatabase else None

    @property
    def cylindrical_gear_agma_material_database(self) -> '_373.CylindricalGearAGMAMaterialDatabase':
        '''CylindricalGearAGMAMaterialDatabase: 'CylindricalGearAGMAMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_373.CylindricalGearAGMAMaterialDatabase)(self.wrapped.CylindricalGearAGMAMaterialDatabase) if self.wrapped.CylindricalGearAGMAMaterialDatabase else None

    @property
    def cylindrical_gear_iso_material_database(self) -> '_374.CylindricalGearISOMaterialDatabase':
        '''CylindricalGearISOMaterialDatabase: 'CylindricalGearISOMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_374.CylindricalGearISOMaterialDatabase)(self.wrapped.CylindricalGearISOMaterialDatabase) if self.wrapped.CylindricalGearISOMaterialDatabase else None

    @property
    def cylindrical_gear_plastic_material_database(self) -> '_377.CylindricalGearPlasticMaterialDatabase':
        '''CylindricalGearPlasticMaterialDatabase: 'CylindricalGearPlasticMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_377.CylindricalGearPlasticMaterialDatabase)(self.wrapped.CylindricalGearPlasticMaterialDatabase) if self.wrapped.CylindricalGearPlasticMaterialDatabase else None

    @property
    def gear_material_expert_system_factor_settings(self) -> '_380.GearMaterialExpertSystemFactorSettings':
        '''GearMaterialExpertSystemFactorSettings: 'GearMaterialExpertSystemFactorSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_380.GearMaterialExpertSystemFactorSettings)(self.wrapped.GearMaterialExpertSystemFactorSettings) if self.wrapped.GearMaterialExpertSystemFactorSettings else None

    @property
    def isotr1417912001_coefficient_of_friction_constants_database(self) -> '_383.ISOTR1417912001CoefficientOfFrictionConstantsDatabase':
        '''ISOTR1417912001CoefficientOfFrictionConstantsDatabase: 'ISOTR1417912001CoefficientOfFrictionConstantsDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_383.ISOTR1417912001CoefficientOfFrictionConstantsDatabase)(self.wrapped.ISOTR1417912001CoefficientOfFrictionConstantsDatabase) if self.wrapped.ISOTR1417912001CoefficientOfFrictionConstantsDatabase else None

    @property
    def klingelnberg_conical_gear_material_database(self) -> '_384.KlingelnbergConicalGearMaterialDatabase':
        '''KlingelnbergConicalGearMaterialDatabase: 'KlingelnbergConicalGearMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_384.KlingelnbergConicalGearMaterialDatabase)(self.wrapped.KlingelnbergConicalGearMaterialDatabase) if self.wrapped.KlingelnbergConicalGearMaterialDatabase else None

    @property
    def raw_material_database(self) -> '_391.RawMaterialDatabase':
        '''RawMaterialDatabase: 'RawMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_391.RawMaterialDatabase)(self.wrapped.RawMaterialDatabase) if self.wrapped.RawMaterialDatabase else None

    @property
    def pocketing_power_loss_coefficients_database(self) -> '_145.PocketingPowerLossCoefficientsDatabase':
        '''PocketingPowerLossCoefficientsDatabase: 'PocketingPowerLossCoefficientsDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_145.PocketingPowerLossCoefficientsDatabase)(self.wrapped.PocketingPowerLossCoefficientsDatabase) if self.wrapped.PocketingPowerLossCoefficientsDatabase else None

    @property
    def cylindrical_gear_rating_settings(self) -> '_261.CylindricalGearRatingSettings':
        '''CylindricalGearRatingSettings: 'CylindricalGearRatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_261.CylindricalGearRatingSettings)(self.wrapped.CylindricalGearRatingSettings) if self.wrapped.CylindricalGearRatingSettings else None

    @property
    def cylindrical_plastic_gear_rating_settings(self) -> '_268.CylindricalPlasticGearRatingSettings':
        '''CylindricalPlasticGearRatingSettings: 'CylindricalPlasticGearRatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_268.CylindricalPlasticGearRatingSettings)(self.wrapped.CylindricalPlasticGearRatingSettings) if self.wrapped.CylindricalPlasticGearRatingSettings else None

    @property
    def bearing_material_database(self) -> '_53.BearingMaterialDatabase':
        '''BearingMaterialDatabase: 'BearingMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_53.BearingMaterialDatabase)(self.wrapped.BearingMaterialDatabase) if self.wrapped.BearingMaterialDatabase else None

    @property
    def component_material_database(self) -> '_54.ComponentMaterialDatabase':
        '''ComponentMaterialDatabase: 'ComponentMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_54.ComponentMaterialDatabase)(self.wrapped.ComponentMaterialDatabase) if self.wrapped.ComponentMaterialDatabase else None

    @property
    def lubrication_detail_database(self) -> '_75.LubricationDetailDatabase':
        '''LubricationDetailDatabase: 'LubricationDetailDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_75.LubricationDetailDatabase)(self.wrapped.LubricationDetailDatabase) if self.wrapped.LubricationDetailDatabase else None

    @property
    def materials_settings(self) -> '_78.MaterialsSettings':
        '''MaterialsSettings: 'MaterialsSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_78.MaterialsSettings)(self.wrapped.MaterialsSettings) if self.wrapped.MaterialsSettings else None

    @property
    def analysis_settings(self) -> '_1359.AnalysisSettings':
        '''AnalysisSettings: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1359.AnalysisSettings)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings else None

    @property
    def fe_user_settings(self) -> '_1374.FEUserSettings':
        '''FEUserSettings: 'FEUserSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1374.FEUserSettings)(self.wrapped.FEUserSettings) if self.wrapped.FEUserSettings else None

    @property
    def shaft_material_database(self) -> '_25.ShaftMaterialDatabase':
        '''ShaftMaterialDatabase: 'ShaftMaterialDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_25.ShaftMaterialDatabase)(self.wrapped.ShaftMaterialDatabase) if self.wrapped.ShaftMaterialDatabase else None

    @property
    def shaft_settings(self) -> '_37.ShaftSettings':
        '''ShaftSettings: 'ShaftSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_37.ShaftSettings)(self.wrapped.ShaftSettings) if self.wrapped.ShaftSettings else None

    @property
    def electric_machine_detail_database(self) -> '_6102.ElectricMachineDetailDatabase':
        '''ElectricMachineDetailDatabase: 'ElectricMachineDetailDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6102.ElectricMachineDetailDatabase)(self.wrapped.ElectricMachineDetailDatabase) if self.wrapped.ElectricMachineDetailDatabase else None

    @property
    def conical_gear_optimization_strategy_database(self) -> '_1815.ConicalGearOptimizationStrategyDatabase':
        '''ConicalGearOptimizationStrategyDatabase: 'ConicalGearOptimizationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1815.ConicalGearOptimizationStrategyDatabase)(self.wrapped.ConicalGearOptimizationStrategyDatabase) if self.wrapped.ConicalGearOptimizationStrategyDatabase else None

    @property
    def optimization_strategy_database(self) -> '_1824.OptimizationStrategyDatabase':
        '''OptimizationStrategyDatabase: 'OptimizationStrategyDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1824.OptimizationStrategyDatabase)(self.wrapped.OptimizationStrategyDatabase) if self.wrapped.OptimizationStrategyDatabase else None

    @property
    def supercharger_rotor_set_database(self) -> '_2103.SuperchargerRotorSetDatabase':
        '''SuperchargerRotorSetDatabase: 'SuperchargerRotorSetDatabase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2103.SuperchargerRotorSetDatabase)(self.wrapped.SuperchargerRotorSetDatabase) if self.wrapped.SuperchargerRotorSetDatabase else None

    @property
    def planet_carrier_settings(self) -> '_2011.PlanetCarrierSettings':
        '''PlanetCarrierSettings: 'PlanetCarrierSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.PlanetCarrierSettings)(self.wrapped.PlanetCarrierSettings) if self.wrapped.PlanetCarrierSettings else None

    @property
    def cad_export_settings(self) -> '_1345.CADExportSettings':
        '''CADExportSettings: 'CADExportSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1345.CADExportSettings)(self.wrapped.CADExportSettings) if self.wrapped.CADExportSettings else None

    @property
    def database_settings(self) -> '_1340.DatabaseSettings':
        '''DatabaseSettings: 'DatabaseSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1340.DatabaseSettings)(self.wrapped.DatabaseSettings) if self.wrapped.DatabaseSettings else None

    @property
    def program_settings(self) -> '_1141.ProgramSettings':
        '''ProgramSettings: 'ProgramSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1141.ProgramSettings)(self.wrapped.ProgramSettings) if self.wrapped.ProgramSettings else None

    @property
    def pushbullet_settings(self) -> '_1142.PushbulletSettings':
        '''PushbulletSettings: 'PushbulletSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1142.PushbulletSettings)(self.wrapped.PushbulletSettings) if self.wrapped.PushbulletSettings else None

    @property
    def scripting_setup(self) -> '_1264.ScriptingSetup':
        '''ScriptingSetup: 'ScriptingSetup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1264.ScriptingSetup)(self.wrapped.ScriptingSetup) if self.wrapped.ScriptingSetup else None

    @property
    def measurement_settings(self) -> '_1151.MeasurementSettings':
        '''MeasurementSettings: 'MeasurementSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1151.MeasurementSettings)(self.wrapped.MeasurementSettings) if self.wrapped.MeasurementSettings else None
