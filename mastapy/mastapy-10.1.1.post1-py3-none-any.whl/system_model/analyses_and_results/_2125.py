'''_2125.py

CompoundModalAnalysisAnalysis
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
from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
    _3022, _3023, _3024, _3025,
    _3026, _3027, _3028, _3029,
    _3030, _3031, _3032, _3033,
    _3034, _3035, _3036, _3037,
    _3038, _3039, _3040, _3041,
    _3042, _3043, _3044, _3045,
    _3046, _3047, _3048, _3049,
    _3050, _3051, _3052, _3053,
    _3054, _3055, _3056, _3057,
    _3058, _3059, _3060, _3061,
    _3062, _3063, _3064, _3065,
    _3066, _3067, _3068, _3069,
    _3070, _3071, _3072, _3073,
    _3074, _3075, _3076, _3077,
    _3078, _3079, _3080, _3081,
    _3082, _3083, _3084, _3085,
    _3086, _3087, _3088, _3089,
    _3090, _3091, _3092, _3093,
    _3094, _3095, _3096, _3097,
    _3098, _3099, _3100, _3101,
    _3102, _3103, _3104, _3105,
    _3106, _3107, _3108, _3109,
    _3110, _3111, _3112, _3113,
    _3114, _3115, _3116, _3117,
    _3118, _3119, _3120, _3121,
    _3122, _3123, _3124, _3125,
    _3126, _3127, _3128, _3129,
    _3130, _3131, _3132, _3133,
    _3134, _3135, _3136, _3137,
    _3138, _3139
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

_COMPOUND_MODAL_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundModalAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundModalAnalysisAnalysis',)


class CompoundModalAnalysisAnalysis(_2080.CompoundAnalysis):
    '''CompoundModalAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_MODAL_ANALYSIS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundModalAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1905.AbstractAssembly') -> 'Iterable[_3022.AbstractAssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AbstractAssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3022.AbstractAssemblyCompoundModalAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1906.AbstractShaftOrHousing') -> 'Iterable[_3023.AbstractShaftOrHousingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AbstractShaftOrHousingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3023.AbstractShaftOrHousingCompoundModalAnalysis))

    def results_for_bearing(self, design_entity: '_1908.Bearing') -> 'Iterable[_3024.BearingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BearingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3024.BearingCompoundModalAnalysis))

    def results_for_bolt(self, design_entity: '_1910.Bolt') -> 'Iterable[_3025.BoltCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BoltCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3025.BoltCompoundModalAnalysis))

    def results_for_bolted_joint(self, design_entity: '_1911.BoltedJoint') -> 'Iterable[_3026.BoltedJointCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BoltedJointCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3026.BoltedJointCompoundModalAnalysis))

    def results_for_component(self, design_entity: '_1912.Component') -> 'Iterable[_3027.ComponentCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ComponentCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3027.ComponentCompoundModalAnalysis))

    def results_for_connector(self, design_entity: '_1915.Connector') -> 'Iterable[_3028.ConnectorCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConnectorCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3028.ConnectorCompoundModalAnalysis))

    def results_for_datum(self, design_entity: '_1916.Datum') -> 'Iterable[_3029.DatumCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.DatumCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3029.DatumCompoundModalAnalysis))

    def results_for_external_cad_model(self, design_entity: '_1919.ExternalCADModel') -> 'Iterable[_3030.ExternalCADModelCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ExternalCADModelCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3030.ExternalCADModelCompoundModalAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_1920.FlexiblePinAssembly') -> 'Iterable[_3031.FlexiblePinAssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.FlexiblePinAssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3031.FlexiblePinAssemblyCompoundModalAnalysis))

    def results_for_assembly(self, design_entity: '_1904.Assembly') -> 'Iterable[_3032.AssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3032.AssemblyCompoundModalAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_1921.GuideDxfModel') -> 'Iterable[_3033.GuideDxfModelCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.GuideDxfModelCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3033.GuideDxfModelCompoundModalAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_1924.ImportedFEComponent') -> 'Iterable[_3034.ImportedFEComponentCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ImportedFEComponentCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3034.ImportedFEComponentCompoundModalAnalysis))

    def results_for_mass_disc(self, design_entity: '_1926.MassDisc') -> 'Iterable[_3035.MassDiscCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.MassDiscCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3035.MassDiscCompoundModalAnalysis))

    def results_for_measurement_component(self, design_entity: '_1927.MeasurementComponent') -> 'Iterable[_3036.MeasurementComponentCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.MeasurementComponentCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3036.MeasurementComponentCompoundModalAnalysis))

    def results_for_mountable_component(self, design_entity: '_1928.MountableComponent') -> 'Iterable[_3037.MountableComponentCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.MountableComponentCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3037.MountableComponentCompoundModalAnalysis))

    def results_for_oil_seal(self, design_entity: '_1929.OilSeal') -> 'Iterable[_3038.OilSealCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.OilSealCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3038.OilSealCompoundModalAnalysis))

    def results_for_part(self, design_entity: '_1931.Part') -> 'Iterable[_3039.PartCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PartCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3039.PartCompoundModalAnalysis))

    def results_for_planet_carrier(self, design_entity: '_1932.PlanetCarrier') -> 'Iterable[_3040.PlanetCarrierCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PlanetCarrierCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3040.PlanetCarrierCompoundModalAnalysis))

    def results_for_point_load(self, design_entity: '_1933.PointLoad') -> 'Iterable[_3041.PointLoadCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PointLoadCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3041.PointLoadCompoundModalAnalysis))

    def results_for_power_load(self, design_entity: '_1934.PowerLoad') -> 'Iterable[_3042.PowerLoadCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PowerLoadCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3042.PowerLoadCompoundModalAnalysis))

    def results_for_root_assembly(self, design_entity: '_1935.RootAssembly') -> 'Iterable[_3043.RootAssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.RootAssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3043.RootAssemblyCompoundModalAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_1937.SpecialisedAssembly') -> 'Iterable[_3044.SpecialisedAssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpecialisedAssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3044.SpecialisedAssemblyCompoundModalAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_1938.UnbalancedMass') -> 'Iterable[_3045.UnbalancedMassCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.UnbalancedMassCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3045.UnbalancedMassCompoundModalAnalysis))

    def results_for_virtual_component(self, design_entity: '_1939.VirtualComponent') -> 'Iterable[_3046.VirtualComponentCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.VirtualComponentCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3046.VirtualComponentCompoundModalAnalysis))

    def results_for_shaft(self, design_entity: '_1942.Shaft') -> 'Iterable[_3047.ShaftCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ShaftCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3047.ShaftCompoundModalAnalysis))

    def results_for_concept_gear(self, design_entity: '_1994.ConceptGear') -> 'Iterable[_3048.ConceptGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3048.ConceptGearCompoundModalAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_1977.ConceptGearSet') -> 'Iterable[_3049.ConceptGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3049.ConceptGearSetCompoundModalAnalysis))

    def results_for_face_gear(self, design_entity: '_1997.FaceGear') -> 'Iterable[_3050.FaceGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.FaceGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3050.FaceGearCompoundModalAnalysis))

    def results_for_face_gear_set(self, design_entity: '_1978.FaceGearSet') -> 'Iterable[_3051.FaceGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.FaceGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3051.FaceGearSetCompoundModalAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_1999.AGMAGleasonConicalGear') -> 'Iterable[_3052.AGMAGleasonConicalGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AGMAGleasonConicalGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3052.AGMAGleasonConicalGearCompoundModalAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_1979.AGMAGleasonConicalGearSet') -> 'Iterable[_3053.AGMAGleasonConicalGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AGMAGleasonConicalGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3053.AGMAGleasonConicalGearSetCompoundModalAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2003.BevelDifferentialGear') -> 'Iterable[_3054.BevelDifferentialGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelDifferentialGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3054.BevelDifferentialGearCompoundModalAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_1981.BevelDifferentialGearSet') -> 'Iterable[_3055.BevelDifferentialGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelDifferentialGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3055.BevelDifferentialGearSetCompoundModalAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2008.BevelDifferentialPlanetGear') -> 'Iterable[_3056.BevelDifferentialPlanetGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelDifferentialPlanetGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3056.BevelDifferentialPlanetGearCompoundModalAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2009.BevelDifferentialSunGear') -> 'Iterable[_3057.BevelDifferentialSunGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelDifferentialSunGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3057.BevelDifferentialSunGearCompoundModalAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2001.BevelGear') -> 'Iterable[_3058.BevelGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3058.BevelGearCompoundModalAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_1980.BevelGearSet') -> 'Iterable[_3059.BevelGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3059.BevelGearSetCompoundModalAnalysis))

    def results_for_conical_gear(self, design_entity: '_1995.ConicalGear') -> 'Iterable[_3060.ConicalGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConicalGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3060.ConicalGearCompoundModalAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_1969.ConicalGearSet') -> 'Iterable[_3061.ConicalGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConicalGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3061.ConicalGearSetCompoundModalAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_1996.CylindricalGear') -> 'Iterable[_3062.CylindricalGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CylindricalGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3062.CylindricalGearCompoundModalAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_1968.CylindricalGearSet') -> 'Iterable[_3063.CylindricalGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CylindricalGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3063.CylindricalGearSetCompoundModalAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2014.CylindricalPlanetGear') -> 'Iterable[_3064.CylindricalPlanetGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CylindricalPlanetGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3064.CylindricalPlanetGearCompoundModalAnalysis))

    def results_for_gear(self, design_entity: '_1992.Gear') -> 'Iterable[_3065.GearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.GearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3065.GearCompoundModalAnalysis))

    def results_for_gear_set(self, design_entity: '_1972.GearSet') -> 'Iterable[_3066.GearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.GearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3066.GearSetCompoundModalAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2002.HypoidGear') -> 'Iterable[_3067.HypoidGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.HypoidGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3067.HypoidGearCompoundModalAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_1965.HypoidGearSet') -> 'Iterable[_3068.HypoidGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.HypoidGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3068.HypoidGearSetCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2000.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_3069.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3069.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_1971.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_3070.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3070.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2012.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_3071.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3071.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_1984.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_3072.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3072.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2013.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_3073.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3073.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_3074.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3074.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_1986.PlanetaryGearSet') -> 'Iterable[_3075.PlanetaryGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PlanetaryGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3075.PlanetaryGearSetCompoundModalAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2004.SpiralBevelGear') -> 'Iterable[_3076.SpiralBevelGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpiralBevelGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3076.SpiralBevelGearCompoundModalAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_1966.SpiralBevelGearSet') -> 'Iterable[_3077.SpiralBevelGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpiralBevelGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3077.SpiralBevelGearSetCompoundModalAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2005.StraightBevelDiffGear') -> 'Iterable[_3078.StraightBevelDiffGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelDiffGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3078.StraightBevelDiffGearCompoundModalAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_1982.StraightBevelDiffGearSet') -> 'Iterable[_3079.StraightBevelDiffGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelDiffGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3079.StraightBevelDiffGearSetCompoundModalAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2006.StraightBevelGear') -> 'Iterable[_3080.StraightBevelGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3080.StraightBevelGearCompoundModalAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_1964.StraightBevelGearSet') -> 'Iterable[_3081.StraightBevelGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3081.StraightBevelGearSetCompoundModalAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2010.StraightBevelPlanetGear') -> 'Iterable[_3082.StraightBevelPlanetGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelPlanetGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3082.StraightBevelPlanetGearCompoundModalAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2011.StraightBevelSunGear') -> 'Iterable[_3083.StraightBevelSunGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelSunGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3083.StraightBevelSunGearCompoundModalAnalysis))

    def results_for_worm_gear(self, design_entity: '_1998.WormGear') -> 'Iterable[_3084.WormGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.WormGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3084.WormGearCompoundModalAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_1970.WormGearSet') -> 'Iterable[_3085.WormGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.WormGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3085.WormGearSetCompoundModalAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2007.ZerolBevelGear') -> 'Iterable[_3086.ZerolBevelGearCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ZerolBevelGearCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3086.ZerolBevelGearCompoundModalAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_1983.ZerolBevelGearSet') -> 'Iterable[_3087.ZerolBevelGearSetCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ZerolBevelGearSetCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3087.ZerolBevelGearSetCompoundModalAnalysis))

    def results_for_belt_drive(self, design_entity: '_1973.BeltDrive') -> 'Iterable[_3088.BeltDriveCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BeltDriveCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3088.BeltDriveCompoundModalAnalysis))

    def results_for_clutch(self, design_entity: '_1988.Clutch') -> 'Iterable[_3089.ClutchCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ClutchCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3089.ClutchCompoundModalAnalysis))

    def results_for_clutch_half(self, design_entity: '_2015.ClutchHalf') -> 'Iterable[_3090.ClutchHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ClutchHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3090.ClutchHalfCompoundModalAnalysis))

    def results_for_concept_coupling(self, design_entity: '_1989.ConceptCoupling') -> 'Iterable[_3091.ConceptCouplingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptCouplingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3091.ConceptCouplingCompoundModalAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2016.ConceptCouplingHalf') -> 'Iterable[_3092.ConceptCouplingHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptCouplingHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3092.ConceptCouplingHalfCompoundModalAnalysis))

    def results_for_coupling(self, design_entity: '_1974.Coupling') -> 'Iterable[_3093.CouplingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CouplingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3093.CouplingCompoundModalAnalysis))

    def results_for_coupling_half(self, design_entity: '_1993.CouplingHalf') -> 'Iterable[_3094.CouplingHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CouplingHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3094.CouplingHalfCompoundModalAnalysis))

    def results_for_cvt(self, design_entity: '_1987.CVT') -> 'Iterable[_3095.CVTCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CVTCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3095.CVTCompoundModalAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2023.CVTPulley') -> 'Iterable[_3096.CVTPulleyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CVTPulleyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3096.CVTPulleyCompoundModalAnalysis))

    def results_for_pulley(self, design_entity: '_2017.Pulley') -> 'Iterable[_3097.PulleyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PulleyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3097.PulleyCompoundModalAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_1967.ShaftHubConnection') -> 'Iterable[_3098.ShaftHubConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ShaftHubConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3098.ShaftHubConnectionCompoundModalAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2018.RollingRing') -> 'Iterable[_3099.RollingRingCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.RollingRingCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3099.RollingRingCompoundModalAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_1975.RollingRingAssembly') -> 'Iterable[_3100.RollingRingAssemblyCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.RollingRingAssemblyCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3100.RollingRingAssemblyCompoundModalAnalysis))

    def results_for_spring_damper(self, design_entity: '_1990.SpringDamper') -> 'Iterable[_3101.SpringDamperCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpringDamperCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3101.SpringDamperCompoundModalAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2019.SpringDamperHalf') -> 'Iterable[_3102.SpringDamperHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpringDamperHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3102.SpringDamperHalfCompoundModalAnalysis))

    def results_for_synchroniser(self, design_entity: '_1976.Synchroniser') -> 'Iterable[_3103.SynchroniserCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SynchroniserCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3103.SynchroniserCompoundModalAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2024.SynchroniserHalf') -> 'Iterable[_3104.SynchroniserHalfCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SynchroniserHalfCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3104.SynchroniserHalfCompoundModalAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2020.SynchroniserPart') -> 'Iterable[_3105.SynchroniserPartCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SynchroniserPartCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3105.SynchroniserPartCompoundModalAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2025.SynchroniserSleeve') -> 'Iterable[_3106.SynchroniserSleeveCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SynchroniserSleeveCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3106.SynchroniserSleeveCompoundModalAnalysis))

    def results_for_torque_converter(self, design_entity: '_1991.TorqueConverter') -> 'Iterable[_3107.TorqueConverterCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.TorqueConverterCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3107.TorqueConverterCompoundModalAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2021.TorqueConverterPump') -> 'Iterable[_3108.TorqueConverterPumpCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.TorqueConverterPumpCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3108.TorqueConverterPumpCompoundModalAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2022.TorqueConverterTurbine') -> 'Iterable[_3109.TorqueConverterTurbineCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.TorqueConverterTurbineCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3109.TorqueConverterTurbineCompoundModalAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1765.CVTBeltConnection') -> 'Iterable[_3110.CVTBeltConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CVTBeltConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3110.CVTBeltConnectionCompoundModalAnalysis))

    def results_for_belt_connection(self, design_entity: '_1760.BeltConnection') -> 'Iterable[_3111.BeltConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BeltConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3111.BeltConnectionCompoundModalAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1761.CoaxialConnection') -> 'Iterable[_3112.CoaxialConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CoaxialConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3112.CoaxialConnectionCompoundModalAnalysis))

    def results_for_connection(self, design_entity: '_1764.Connection') -> 'Iterable[_3113.ConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3113.ConnectionCompoundModalAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1773.InterMountableComponentConnection') -> 'Iterable[_3114.InterMountableComponentConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.InterMountableComponentConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3114.InterMountableComponentConnectionCompoundModalAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1776.PlanetaryConnection') -> 'Iterable[_3115.PlanetaryConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.PlanetaryConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3115.PlanetaryConnectionCompoundModalAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1780.RollingRingConnection') -> 'Iterable[_3116.RollingRingConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.RollingRingConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3116.RollingRingConnectionCompoundModalAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1784.ShaftToMountableComponentConnection') -> 'Iterable[_3117.ShaftToMountableComponentConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ShaftToMountableComponentConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3117.ShaftToMountableComponentConnectionCompoundModalAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1822.ClutchConnection') -> 'Iterable[_3118.ClutchConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ClutchConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3118.ClutchConnectionCompoundModalAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1824.ConceptCouplingConnection') -> 'Iterable[_3119.ConceptCouplingConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptCouplingConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3119.ConceptCouplingConnectionCompoundModalAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1826.CouplingConnection') -> 'Iterable[_3120.CouplingConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CouplingConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3120.CouplingConnectionCompoundModalAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1828.SpringDamperConnection') -> 'Iterable[_3121.SpringDamperConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpringDamperConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3121.SpringDamperConnectionCompoundModalAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1830.TorqueConverterConnection') -> 'Iterable[_3122.TorqueConverterConnectionCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.TorqueConverterConnectionCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3122.TorqueConverterConnectionCompoundModalAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1790.BevelDifferentialGearMesh') -> 'Iterable[_3123.BevelDifferentialGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelDifferentialGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3123.BevelDifferentialGearMeshCompoundModalAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1794.ConceptGearMesh') -> 'Iterable[_3124.ConceptGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConceptGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3124.ConceptGearMeshCompoundModalAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1800.FaceGearMesh') -> 'Iterable[_3125.FaceGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.FaceGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3125.FaceGearMeshCompoundModalAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1814.StraightBevelDiffGearMesh') -> 'Iterable[_3126.StraightBevelDiffGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelDiffGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3126.StraightBevelDiffGearMeshCompoundModalAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1792.BevelGearMesh') -> 'Iterable[_3127.BevelGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.BevelGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3127.BevelGearMeshCompoundModalAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1796.ConicalGearMesh') -> 'Iterable[_3128.ConicalGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConicalGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3128.ConicalGearMeshCompoundModalAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1788.AGMAGleasonConicalGearMesh') -> 'Iterable[_3129.AGMAGleasonConicalGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.AGMAGleasonConicalGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3129.AGMAGleasonConicalGearMeshCompoundModalAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1798.CylindricalGearMesh') -> 'Iterable[_3130.CylindricalGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.CylindricalGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3130.CylindricalGearMeshCompoundModalAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1804.HypoidGearMesh') -> 'Iterable[_3131.HypoidGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.HypoidGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3131.HypoidGearMeshCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1807.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_3132.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3132.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1808.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_3133.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3133.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_3134.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3134.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1812.SpiralBevelGearMesh') -> 'Iterable[_3135.SpiralBevelGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.SpiralBevelGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3135.SpiralBevelGearMeshCompoundModalAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1816.StraightBevelGearMesh') -> 'Iterable[_3136.StraightBevelGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.StraightBevelGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3136.StraightBevelGearMeshCompoundModalAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1818.WormGearMesh') -> 'Iterable[_3137.WormGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.WormGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3137.WormGearMeshCompoundModalAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1820.ZerolBevelGearMesh') -> 'Iterable[_3138.ZerolBevelGearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.ZerolBevelGearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3138.ZerolBevelGearMeshCompoundModalAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1802.GearMesh') -> 'Iterable[_3139.GearMeshCompoundModalAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.modal_analyses.compound.GearMeshCompoundModalAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3139.GearMeshCompoundModalAnalysis))
