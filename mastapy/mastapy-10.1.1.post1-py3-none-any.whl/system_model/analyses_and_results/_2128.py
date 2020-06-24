'''_2128.py

CompoundPowerFlowAnalysis
'''


from typing import Iterable

from mastapy.system_model.part_model import (
    _1905, _1906, _1908, _1910,
    _1911, _1912, _1915, _1916,
    _1919, _1920, _1904, _1921,
    _1924, _1926, _1927, _1928,
    _1929, _1931, _1932, _1933,
    _1934, _1935, _1937, _1938,
    _1939
)
from mastapy.system_model.analyses_and_results.power_flows.compound import (
    _3140, _3141, _3142, _3143,
    _3144, _3145, _3146, _3147,
    _3148, _3149, _3150, _3151,
    _3152, _3153, _3154, _3155,
    _3156, _3157, _3158, _3159,
    _3160, _2958, _3161, _3162,
    _3163, _3164, _3165, _3166,
    _3167, _3168, _3169, _3170,
    _3171, _3172, _3173, _3174,
    _3175, _3176, _3177, _3178,
    _3179, _3180, _3181, _3182,
    _3183, _3184, _3185, _3186,
    _3187, _3188, _3189, _3190,
    _3191, _3192, _3193, _3194,
    _3195, _3196, _3197, _3198,
    _3199, _3200, _3201, _3202,
    _3203, _3204, _3205, _3206,
    _3207, _3208, _3209, _3210,
    _3211, _3212, _3213, _3214,
    _3215, _3216, _3217, _3218,
    _3219, _3220, _3221, _3222,
    _3223, _3224, _3225, _3226,
    _3227, _3228, _3229, _3230,
    _3231, _3232, _3233, _3234,
    _3235, _3236, _3237, _3238,
    _3239, _3240, _3241, _3242,
    _3243, _3244, _3245, _3246,
    _3247, _3248, _3249, _3250,
    _3251, _3252, _3253, _3254,
    _3255, _3256
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _1942
from mastapy.system_model.part_model.gears import (
    _1994, _1977, _1997, _1978,
    _1999, _1979, _2003, _1981,
    _2008, _2009, _2001, _1980,
    _1995, _1969, _1996, _1968,
    _2014, _1992, _1972, _2002,
    _1965, _2000, _1971, _2012,
    _1984, _2013, _1985, _1986,
    _2004, _1966, _2005, _1982,
    _2006, _1964, _2010, _2011,
    _1998, _1970, _2007, _1983
)
from mastapy.system_model.part_model.couplings import (
    _1973, _1988, _2015, _1989,
    _2016, _1974, _1993, _1987,
    _2023, _2017, _1967, _2018,
    _1975, _1990, _2019, _1976,
    _2024, _2020, _2025, _1991,
    _2021, _2022
)
from mastapy.system_model.connections_and_sockets import (
    _1765, _1760, _1761, _1764,
    _1773, _1776, _1780, _1784
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1822, _1824, _1826, _1828,
    _1830
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1790, _1794, _1800, _1814,
    _1792, _1796, _1788, _1798,
    _1804, _1807, _1808, _1809,
    _1812, _1816, _1818, _1820,
    _1802
)
from mastapy.system_model.analyses_and_results import _2080
from mastapy._internal.python_net import python_net_import

_COMPOUND_POWER_FLOW_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundPowerFlowAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundPowerFlowAnalysis',)


class CompoundPowerFlowAnalysis(_2080.CompoundAnalysis):
    '''CompoundPowerFlowAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_POWER_FLOW_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundPowerFlowAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1905.AbstractAssembly') -> 'Iterable[_3140.AbstractAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AbstractAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3140.AbstractAssemblyCompoundPowerFlow))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1906.AbstractShaftOrHousing') -> 'Iterable[_3141.AbstractShaftOrHousingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AbstractShaftOrHousingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3141.AbstractShaftOrHousingCompoundPowerFlow))

    def results_for_bearing(self, design_entity: '_1908.Bearing') -> 'Iterable[_3142.BearingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BearingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3142.BearingCompoundPowerFlow))

    def results_for_bolt(self, design_entity: '_1910.Bolt') -> 'Iterable[_3143.BoltCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BoltCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3143.BoltCompoundPowerFlow))

    def results_for_bolted_joint(self, design_entity: '_1911.BoltedJoint') -> 'Iterable[_3144.BoltedJointCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BoltedJointCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3144.BoltedJointCompoundPowerFlow))

    def results_for_component(self, design_entity: '_1912.Component') -> 'Iterable[_3145.ComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3145.ComponentCompoundPowerFlow))

    def results_for_connector(self, design_entity: '_1915.Connector') -> 'Iterable[_3146.ConnectorCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConnectorCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3146.ConnectorCompoundPowerFlow))

    def results_for_datum(self, design_entity: '_1916.Datum') -> 'Iterable[_3147.DatumCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.DatumCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3147.DatumCompoundPowerFlow))

    def results_for_external_cad_model(self, design_entity: '_1919.ExternalCADModel') -> 'Iterable[_3148.ExternalCADModelCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ExternalCADModelCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3148.ExternalCADModelCompoundPowerFlow))

    def results_for_flexible_pin_assembly(self, design_entity: '_1920.FlexiblePinAssembly') -> 'Iterable[_3149.FlexiblePinAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FlexiblePinAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3149.FlexiblePinAssemblyCompoundPowerFlow))

    def results_for_assembly(self, design_entity: '_1904.Assembly') -> 'Iterable[_3150.AssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3150.AssemblyCompoundPowerFlow))

    def results_for_guide_dxf_model(self, design_entity: '_1921.GuideDxfModel') -> 'Iterable[_3151.GuideDxfModelCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GuideDxfModelCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3151.GuideDxfModelCompoundPowerFlow))

    def results_for_imported_fe_component(self, design_entity: '_1924.ImportedFEComponent') -> 'Iterable[_3152.ImportedFEComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ImportedFEComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3152.ImportedFEComponentCompoundPowerFlow))

    def results_for_mass_disc(self, design_entity: '_1926.MassDisc') -> 'Iterable[_3153.MassDiscCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MassDiscCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3153.MassDiscCompoundPowerFlow))

    def results_for_measurement_component(self, design_entity: '_1927.MeasurementComponent') -> 'Iterable[_3154.MeasurementComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MeasurementComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3154.MeasurementComponentCompoundPowerFlow))

    def results_for_mountable_component(self, design_entity: '_1928.MountableComponent') -> 'Iterable[_3155.MountableComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MountableComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3155.MountableComponentCompoundPowerFlow))

    def results_for_oil_seal(self, design_entity: '_1929.OilSeal') -> 'Iterable[_3156.OilSealCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.OilSealCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3156.OilSealCompoundPowerFlow))

    def results_for_part(self, design_entity: '_1931.Part') -> 'Iterable[_3157.PartCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3157.PartCompoundPowerFlow))

    def results_for_planet_carrier(self, design_entity: '_1932.PlanetCarrier') -> 'Iterable[_3158.PlanetCarrierCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetCarrierCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3158.PlanetCarrierCompoundPowerFlow))

    def results_for_point_load(self, design_entity: '_1933.PointLoad') -> 'Iterable[_3159.PointLoadCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PointLoadCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3159.PointLoadCompoundPowerFlow))

    def results_for_power_load(self, design_entity: '_1934.PowerLoad') -> 'Iterable[_3160.PowerLoadCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PowerLoadCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3160.PowerLoadCompoundPowerFlow))

    def results_for_root_assembly(self, design_entity: '_1935.RootAssembly') -> 'Iterable[_2958.RootAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RootAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2958.RootAssemblyCompoundPowerFlow))

    def results_for_specialised_assembly(self, design_entity: '_1937.SpecialisedAssembly') -> 'Iterable[_3161.SpecialisedAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpecialisedAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3161.SpecialisedAssemblyCompoundPowerFlow))

    def results_for_unbalanced_mass(self, design_entity: '_1938.UnbalancedMass') -> 'Iterable[_3162.UnbalancedMassCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.UnbalancedMassCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3162.UnbalancedMassCompoundPowerFlow))

    def results_for_virtual_component(self, design_entity: '_1939.VirtualComponent') -> 'Iterable[_3163.VirtualComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.VirtualComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3163.VirtualComponentCompoundPowerFlow))

    def results_for_shaft(self, design_entity: '_1942.Shaft') -> 'Iterable[_3164.ShaftCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3164.ShaftCompoundPowerFlow))

    def results_for_concept_gear(self, design_entity: '_1994.ConceptGear') -> 'Iterable[_3165.ConceptGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3165.ConceptGearCompoundPowerFlow))

    def results_for_concept_gear_set(self, design_entity: '_1977.ConceptGearSet') -> 'Iterable[_3166.ConceptGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3166.ConceptGearSetCompoundPowerFlow))

    def results_for_face_gear(self, design_entity: '_1997.FaceGear') -> 'Iterable[_3167.FaceGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3167.FaceGearCompoundPowerFlow))

    def results_for_face_gear_set(self, design_entity: '_1978.FaceGearSet') -> 'Iterable[_3168.FaceGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3168.FaceGearSetCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_1999.AGMAGleasonConicalGear') -> 'Iterable[_3169.AGMAGleasonConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3169.AGMAGleasonConicalGearCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_1979.AGMAGleasonConicalGearSet') -> 'Iterable[_3170.AGMAGleasonConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3170.AGMAGleasonConicalGearSetCompoundPowerFlow))

    def results_for_bevel_differential_gear(self, design_entity: '_2003.BevelDifferentialGear') -> 'Iterable[_3171.BevelDifferentialGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3171.BevelDifferentialGearCompoundPowerFlow))

    def results_for_bevel_differential_gear_set(self, design_entity: '_1981.BevelDifferentialGearSet') -> 'Iterable[_3172.BevelDifferentialGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3172.BevelDifferentialGearSetCompoundPowerFlow))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2008.BevelDifferentialPlanetGear') -> 'Iterable[_3173.BevelDifferentialPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3173.BevelDifferentialPlanetGearCompoundPowerFlow))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2009.BevelDifferentialSunGear') -> 'Iterable[_3174.BevelDifferentialSunGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialSunGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3174.BevelDifferentialSunGearCompoundPowerFlow))

    def results_for_bevel_gear(self, design_entity: '_2001.BevelGear') -> 'Iterable[_3175.BevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3175.BevelGearCompoundPowerFlow))

    def results_for_bevel_gear_set(self, design_entity: '_1980.BevelGearSet') -> 'Iterable[_3176.BevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3176.BevelGearSetCompoundPowerFlow))

    def results_for_conical_gear(self, design_entity: '_1995.ConicalGear') -> 'Iterable[_3177.ConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3177.ConicalGearCompoundPowerFlow))

    def results_for_conical_gear_set(self, design_entity: '_1969.ConicalGearSet') -> 'Iterable[_3178.ConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3178.ConicalGearSetCompoundPowerFlow))

    def results_for_cylindrical_gear(self, design_entity: '_1996.CylindricalGear') -> 'Iterable[_3179.CylindricalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3179.CylindricalGearCompoundPowerFlow))

    def results_for_cylindrical_gear_set(self, design_entity: '_1968.CylindricalGearSet') -> 'Iterable[_3180.CylindricalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3180.CylindricalGearSetCompoundPowerFlow))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2014.CylindricalPlanetGear') -> 'Iterable[_3181.CylindricalPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3181.CylindricalPlanetGearCompoundPowerFlow))

    def results_for_gear(self, design_entity: '_1992.Gear') -> 'Iterable[_3182.GearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3182.GearCompoundPowerFlow))

    def results_for_gear_set(self, design_entity: '_1972.GearSet') -> 'Iterable[_3183.GearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3183.GearSetCompoundPowerFlow))

    def results_for_hypoid_gear(self, design_entity: '_2002.HypoidGear') -> 'Iterable[_3184.HypoidGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3184.HypoidGearCompoundPowerFlow))

    def results_for_hypoid_gear_set(self, design_entity: '_1965.HypoidGearSet') -> 'Iterable[_3185.HypoidGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3185.HypoidGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2000.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_3186.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3186.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_1971.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_3187.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3187.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2012.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_3188.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3188.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_1984.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_3189.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3189.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2013.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_3190.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3190.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_3191.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3191.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow))

    def results_for_planetary_gear_set(self, design_entity: '_1986.PlanetaryGearSet') -> 'Iterable[_3192.PlanetaryGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetaryGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3192.PlanetaryGearSetCompoundPowerFlow))

    def results_for_spiral_bevel_gear(self, design_entity: '_2004.SpiralBevelGear') -> 'Iterable[_3193.SpiralBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3193.SpiralBevelGearCompoundPowerFlow))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_1966.SpiralBevelGearSet') -> 'Iterable[_3194.SpiralBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3194.SpiralBevelGearSetCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2005.StraightBevelDiffGear') -> 'Iterable[_3195.StraightBevelDiffGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3195.StraightBevelDiffGearCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_1982.StraightBevelDiffGearSet') -> 'Iterable[_3196.StraightBevelDiffGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3196.StraightBevelDiffGearSetCompoundPowerFlow))

    def results_for_straight_bevel_gear(self, design_entity: '_2006.StraightBevelGear') -> 'Iterable[_3197.StraightBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3197.StraightBevelGearCompoundPowerFlow))

    def results_for_straight_bevel_gear_set(self, design_entity: '_1964.StraightBevelGearSet') -> 'Iterable[_3198.StraightBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3198.StraightBevelGearSetCompoundPowerFlow))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2010.StraightBevelPlanetGear') -> 'Iterable[_3199.StraightBevelPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3199.StraightBevelPlanetGearCompoundPowerFlow))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2011.StraightBevelSunGear') -> 'Iterable[_3200.StraightBevelSunGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelSunGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3200.StraightBevelSunGearCompoundPowerFlow))

    def results_for_worm_gear(self, design_entity: '_1998.WormGear') -> 'Iterable[_3201.WormGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3201.WormGearCompoundPowerFlow))

    def results_for_worm_gear_set(self, design_entity: '_1970.WormGearSet') -> 'Iterable[_3202.WormGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3202.WormGearSetCompoundPowerFlow))

    def results_for_zerol_bevel_gear(self, design_entity: '_2007.ZerolBevelGear') -> 'Iterable[_3203.ZerolBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3203.ZerolBevelGearCompoundPowerFlow))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_1983.ZerolBevelGearSet') -> 'Iterable[_3204.ZerolBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3204.ZerolBevelGearSetCompoundPowerFlow))

    def results_for_belt_drive(self, design_entity: '_1973.BeltDrive') -> 'Iterable[_3205.BeltDriveCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BeltDriveCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3205.BeltDriveCompoundPowerFlow))

    def results_for_clutch(self, design_entity: '_1988.Clutch') -> 'Iterable[_3206.ClutchCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3206.ClutchCompoundPowerFlow))

    def results_for_clutch_half(self, design_entity: '_2015.ClutchHalf') -> 'Iterable[_3207.ClutchHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3207.ClutchHalfCompoundPowerFlow))

    def results_for_concept_coupling(self, design_entity: '_1989.ConceptCoupling') -> 'Iterable[_3208.ConceptCouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3208.ConceptCouplingCompoundPowerFlow))

    def results_for_concept_coupling_half(self, design_entity: '_2016.ConceptCouplingHalf') -> 'Iterable[_3209.ConceptCouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3209.ConceptCouplingHalfCompoundPowerFlow))

    def results_for_coupling(self, design_entity: '_1974.Coupling') -> 'Iterable[_3210.CouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3210.CouplingCompoundPowerFlow))

    def results_for_coupling_half(self, design_entity: '_1993.CouplingHalf') -> 'Iterable[_3211.CouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3211.CouplingHalfCompoundPowerFlow))

    def results_for_cvt(self, design_entity: '_1987.CVT') -> 'Iterable[_3212.CVTCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3212.CVTCompoundPowerFlow))

    def results_for_cvt_pulley(self, design_entity: '_2023.CVTPulley') -> 'Iterable[_3213.CVTPulleyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTPulleyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3213.CVTPulleyCompoundPowerFlow))

    def results_for_pulley(self, design_entity: '_2017.Pulley') -> 'Iterable[_3214.PulleyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PulleyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3214.PulleyCompoundPowerFlow))

    def results_for_shaft_hub_connection(self, design_entity: '_1967.ShaftHubConnection') -> 'Iterable[_3215.ShaftHubConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftHubConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3215.ShaftHubConnectionCompoundPowerFlow))

    def results_for_rolling_ring(self, design_entity: '_2018.RollingRing') -> 'Iterable[_3216.RollingRingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3216.RollingRingCompoundPowerFlow))

    def results_for_rolling_ring_assembly(self, design_entity: '_1975.RollingRingAssembly') -> 'Iterable[_3217.RollingRingAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3217.RollingRingAssemblyCompoundPowerFlow))

    def results_for_spring_damper(self, design_entity: '_1990.SpringDamper') -> 'Iterable[_3218.SpringDamperCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3218.SpringDamperCompoundPowerFlow))

    def results_for_spring_damper_half(self, design_entity: '_2019.SpringDamperHalf') -> 'Iterable[_3219.SpringDamperHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3219.SpringDamperHalfCompoundPowerFlow))

    def results_for_synchroniser(self, design_entity: '_1976.Synchroniser') -> 'Iterable[_3220.SynchroniserCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3220.SynchroniserCompoundPowerFlow))

    def results_for_synchroniser_half(self, design_entity: '_2024.SynchroniserHalf') -> 'Iterable[_3221.SynchroniserHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3221.SynchroniserHalfCompoundPowerFlow))

    def results_for_synchroniser_part(self, design_entity: '_2020.SynchroniserPart') -> 'Iterable[_3222.SynchroniserPartCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserPartCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3222.SynchroniserPartCompoundPowerFlow))

    def results_for_synchroniser_sleeve(self, design_entity: '_2025.SynchroniserSleeve') -> 'Iterable[_3223.SynchroniserSleeveCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserSleeveCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3223.SynchroniserSleeveCompoundPowerFlow))

    def results_for_torque_converter(self, design_entity: '_1991.TorqueConverter') -> 'Iterable[_3224.TorqueConverterCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3224.TorqueConverterCompoundPowerFlow))

    def results_for_torque_converter_pump(self, design_entity: '_2021.TorqueConverterPump') -> 'Iterable[_3225.TorqueConverterPumpCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterPumpCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3225.TorqueConverterPumpCompoundPowerFlow))

    def results_for_torque_converter_turbine(self, design_entity: '_2022.TorqueConverterTurbine') -> 'Iterable[_3226.TorqueConverterTurbineCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterTurbineCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3226.TorqueConverterTurbineCompoundPowerFlow))

    def results_for_cvt_belt_connection(self, design_entity: '_1765.CVTBeltConnection') -> 'Iterable[_3227.CVTBeltConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTBeltConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3227.CVTBeltConnectionCompoundPowerFlow))

    def results_for_belt_connection(self, design_entity: '_1760.BeltConnection') -> 'Iterable[_3228.BeltConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BeltConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3228.BeltConnectionCompoundPowerFlow))

    def results_for_coaxial_connection(self, design_entity: '_1761.CoaxialConnection') -> 'Iterable[_3229.CoaxialConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CoaxialConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3229.CoaxialConnectionCompoundPowerFlow))

    def results_for_connection(self, design_entity: '_1764.Connection') -> 'Iterable[_3230.ConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3230.ConnectionCompoundPowerFlow))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1773.InterMountableComponentConnection') -> 'Iterable[_3231.InterMountableComponentConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.InterMountableComponentConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3231.InterMountableComponentConnectionCompoundPowerFlow))

    def results_for_planetary_connection(self, design_entity: '_1776.PlanetaryConnection') -> 'Iterable[_3232.PlanetaryConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetaryConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3232.PlanetaryConnectionCompoundPowerFlow))

    def results_for_rolling_ring_connection(self, design_entity: '_1780.RollingRingConnection') -> 'Iterable[_3233.RollingRingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3233.RollingRingConnectionCompoundPowerFlow))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1784.ShaftToMountableComponentConnection') -> 'Iterable[_3234.ShaftToMountableComponentConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftToMountableComponentConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3234.ShaftToMountableComponentConnectionCompoundPowerFlow))

    def results_for_clutch_connection(self, design_entity: '_1822.ClutchConnection') -> 'Iterable[_3235.ClutchConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3235.ClutchConnectionCompoundPowerFlow))

    def results_for_concept_coupling_connection(self, design_entity: '_1824.ConceptCouplingConnection') -> 'Iterable[_3236.ConceptCouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3236.ConceptCouplingConnectionCompoundPowerFlow))

    def results_for_coupling_connection(self, design_entity: '_1826.CouplingConnection') -> 'Iterable[_3237.CouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3237.CouplingConnectionCompoundPowerFlow))

    def results_for_spring_damper_connection(self, design_entity: '_1828.SpringDamperConnection') -> 'Iterable[_3238.SpringDamperConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3238.SpringDamperConnectionCompoundPowerFlow))

    def results_for_torque_converter_connection(self, design_entity: '_1830.TorqueConverterConnection') -> 'Iterable[_3239.TorqueConverterConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3239.TorqueConverterConnectionCompoundPowerFlow))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1790.BevelDifferentialGearMesh') -> 'Iterable[_3240.BevelDifferentialGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3240.BevelDifferentialGearMeshCompoundPowerFlow))

    def results_for_concept_gear_mesh(self, design_entity: '_1794.ConceptGearMesh') -> 'Iterable[_3241.ConceptGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3241.ConceptGearMeshCompoundPowerFlow))

    def results_for_face_gear_mesh(self, design_entity: '_1800.FaceGearMesh') -> 'Iterable[_3242.FaceGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3242.FaceGearMeshCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1814.StraightBevelDiffGearMesh') -> 'Iterable[_3243.StraightBevelDiffGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3243.StraightBevelDiffGearMeshCompoundPowerFlow))

    def results_for_bevel_gear_mesh(self, design_entity: '_1792.BevelGearMesh') -> 'Iterable[_3244.BevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3244.BevelGearMeshCompoundPowerFlow))

    def results_for_conical_gear_mesh(self, design_entity: '_1796.ConicalGearMesh') -> 'Iterable[_3245.ConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3245.ConicalGearMeshCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1788.AGMAGleasonConicalGearMesh') -> 'Iterable[_3246.AGMAGleasonConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3246.AGMAGleasonConicalGearMeshCompoundPowerFlow))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1798.CylindricalGearMesh') -> 'Iterable[_3247.CylindricalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3247.CylindricalGearMeshCompoundPowerFlow))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1804.HypoidGearMesh') -> 'Iterable[_3248.HypoidGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3248.HypoidGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1807.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_3249.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3249.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1808.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_3250.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3250.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_3251.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3251.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1812.SpiralBevelGearMesh') -> 'Iterable[_3252.SpiralBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3252.SpiralBevelGearMeshCompoundPowerFlow))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1816.StraightBevelGearMesh') -> 'Iterable[_3253.StraightBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3253.StraightBevelGearMeshCompoundPowerFlow))

    def results_for_worm_gear_mesh(self, design_entity: '_1818.WormGearMesh') -> 'Iterable[_3254.WormGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3254.WormGearMeshCompoundPowerFlow))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1820.ZerolBevelGearMesh') -> 'Iterable[_3255.ZerolBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3255.ZerolBevelGearMeshCompoundPowerFlow))

    def results_for_gear_mesh(self, design_entity: '_1802.GearMesh') -> 'Iterable[_3256.GearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3256.GearMeshCompoundPowerFlow))
