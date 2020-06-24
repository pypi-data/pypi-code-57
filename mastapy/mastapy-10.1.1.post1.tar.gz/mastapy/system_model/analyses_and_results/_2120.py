'''_2120.py

CompoundGearWhineAnalysisAnalysis
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
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import (
    _2840, _2841, _2842, _2843,
    _2844, _2845, _2846, _2847,
    _2848, _2849, _2850, _2851,
    _2852, _2853, _2854, _2855,
    _2856, _2857, _2858, _2859,
    _2860, _2861, _2862, _2863,
    _2864, _2865, _2866, _2867,
    _2868, _2869, _2870, _2871,
    _2872, _2873, _2874, _2875,
    _2876, _2877, _2878, _2879,
    _2880, _2881, _2882, _2883,
    _2884, _2885, _2886, _2887,
    _2888, _2889, _2890, _2891,
    _2892, _2893, _2894, _2895,
    _2896, _2897, _2898, _2899,
    _2900, _2901, _2902, _2903,
    _2904, _2905, _2906, _2907,
    _2908, _2909, _2910, _2911,
    _2912, _2913, _2914, _2915,
    _2916, _2917, _2918, _2919,
    _2920, _2921, _2922, _2923,
    _2924, _2925, _2926, _2927,
    _2928, _2929, _2930, _2931,
    _2932, _2933, _2934, _2935,
    _2936, _2937, _2938, _2939,
    _2940, _2941, _2942, _2943,
    _2944, _2945, _2946, _2947,
    _2948, _2949, _2950, _2951,
    _2952, _2953, _2954, _2955,
    _2956, _2957
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

_COMPOUND_GEAR_WHINE_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundGearWhineAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundGearWhineAnalysisAnalysis',)


class CompoundGearWhineAnalysisAnalysis(_2080.CompoundAnalysis):
    '''CompoundGearWhineAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_GEAR_WHINE_ANALYSIS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundGearWhineAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1905.AbstractAssembly') -> 'Iterable[_2840.AbstractAssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AbstractAssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2840.AbstractAssemblyCompoundGearWhineAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1906.AbstractShaftOrHousing') -> 'Iterable[_2841.AbstractShaftOrHousingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AbstractShaftOrHousingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2841.AbstractShaftOrHousingCompoundGearWhineAnalysis))

    def results_for_bearing(self, design_entity: '_1908.Bearing') -> 'Iterable[_2842.BearingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BearingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2842.BearingCompoundGearWhineAnalysis))

    def results_for_bolt(self, design_entity: '_1910.Bolt') -> 'Iterable[_2843.BoltCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BoltCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2843.BoltCompoundGearWhineAnalysis))

    def results_for_bolted_joint(self, design_entity: '_1911.BoltedJoint') -> 'Iterable[_2844.BoltedJointCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BoltedJointCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2844.BoltedJointCompoundGearWhineAnalysis))

    def results_for_component(self, design_entity: '_1912.Component') -> 'Iterable[_2845.ComponentCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ComponentCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2845.ComponentCompoundGearWhineAnalysis))

    def results_for_connector(self, design_entity: '_1915.Connector') -> 'Iterable[_2846.ConnectorCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConnectorCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2846.ConnectorCompoundGearWhineAnalysis))

    def results_for_datum(self, design_entity: '_1916.Datum') -> 'Iterable[_2847.DatumCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.DatumCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2847.DatumCompoundGearWhineAnalysis))

    def results_for_external_cad_model(self, design_entity: '_1919.ExternalCADModel') -> 'Iterable[_2848.ExternalCADModelCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ExternalCADModelCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2848.ExternalCADModelCompoundGearWhineAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_1920.FlexiblePinAssembly') -> 'Iterable[_2849.FlexiblePinAssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.FlexiblePinAssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2849.FlexiblePinAssemblyCompoundGearWhineAnalysis))

    def results_for_assembly(self, design_entity: '_1904.Assembly') -> 'Iterable[_2850.AssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2850.AssemblyCompoundGearWhineAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_1921.GuideDxfModel') -> 'Iterable[_2851.GuideDxfModelCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.GuideDxfModelCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2851.GuideDxfModelCompoundGearWhineAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_1924.ImportedFEComponent') -> 'Iterable[_2852.ImportedFEComponentCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ImportedFEComponentCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2852.ImportedFEComponentCompoundGearWhineAnalysis))

    def results_for_mass_disc(self, design_entity: '_1926.MassDisc') -> 'Iterable[_2853.MassDiscCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.MassDiscCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2853.MassDiscCompoundGearWhineAnalysis))

    def results_for_measurement_component(self, design_entity: '_1927.MeasurementComponent') -> 'Iterable[_2854.MeasurementComponentCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.MeasurementComponentCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2854.MeasurementComponentCompoundGearWhineAnalysis))

    def results_for_mountable_component(self, design_entity: '_1928.MountableComponent') -> 'Iterable[_2855.MountableComponentCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.MountableComponentCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2855.MountableComponentCompoundGearWhineAnalysis))

    def results_for_oil_seal(self, design_entity: '_1929.OilSeal') -> 'Iterable[_2856.OilSealCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.OilSealCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2856.OilSealCompoundGearWhineAnalysis))

    def results_for_part(self, design_entity: '_1931.Part') -> 'Iterable[_2857.PartCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PartCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2857.PartCompoundGearWhineAnalysis))

    def results_for_planet_carrier(self, design_entity: '_1932.PlanetCarrier') -> 'Iterable[_2858.PlanetCarrierCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PlanetCarrierCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2858.PlanetCarrierCompoundGearWhineAnalysis))

    def results_for_point_load(self, design_entity: '_1933.PointLoad') -> 'Iterable[_2859.PointLoadCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PointLoadCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2859.PointLoadCompoundGearWhineAnalysis))

    def results_for_power_load(self, design_entity: '_1934.PowerLoad') -> 'Iterable[_2860.PowerLoadCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PowerLoadCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2860.PowerLoadCompoundGearWhineAnalysis))

    def results_for_root_assembly(self, design_entity: '_1935.RootAssembly') -> 'Iterable[_2861.RootAssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.RootAssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2861.RootAssemblyCompoundGearWhineAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_1937.SpecialisedAssembly') -> 'Iterable[_2862.SpecialisedAssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpecialisedAssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2862.SpecialisedAssemblyCompoundGearWhineAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_1938.UnbalancedMass') -> 'Iterable[_2863.UnbalancedMassCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.UnbalancedMassCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2863.UnbalancedMassCompoundGearWhineAnalysis))

    def results_for_virtual_component(self, design_entity: '_1939.VirtualComponent') -> 'Iterable[_2864.VirtualComponentCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.VirtualComponentCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2864.VirtualComponentCompoundGearWhineAnalysis))

    def results_for_shaft(self, design_entity: '_1942.Shaft') -> 'Iterable[_2865.ShaftCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ShaftCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2865.ShaftCompoundGearWhineAnalysis))

    def results_for_concept_gear(self, design_entity: '_1994.ConceptGear') -> 'Iterable[_2866.ConceptGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2866.ConceptGearCompoundGearWhineAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_1977.ConceptGearSet') -> 'Iterable[_2867.ConceptGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2867.ConceptGearSetCompoundGearWhineAnalysis))

    def results_for_face_gear(self, design_entity: '_1997.FaceGear') -> 'Iterable[_2868.FaceGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.FaceGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2868.FaceGearCompoundGearWhineAnalysis))

    def results_for_face_gear_set(self, design_entity: '_1978.FaceGearSet') -> 'Iterable[_2869.FaceGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.FaceGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2869.FaceGearSetCompoundGearWhineAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_1999.AGMAGleasonConicalGear') -> 'Iterable[_2870.AGMAGleasonConicalGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AGMAGleasonConicalGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2870.AGMAGleasonConicalGearCompoundGearWhineAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_1979.AGMAGleasonConicalGearSet') -> 'Iterable[_2871.AGMAGleasonConicalGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AGMAGleasonConicalGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2871.AGMAGleasonConicalGearSetCompoundGearWhineAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2003.BevelDifferentialGear') -> 'Iterable[_2872.BevelDifferentialGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelDifferentialGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2872.BevelDifferentialGearCompoundGearWhineAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_1981.BevelDifferentialGearSet') -> 'Iterable[_2873.BevelDifferentialGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelDifferentialGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2873.BevelDifferentialGearSetCompoundGearWhineAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2008.BevelDifferentialPlanetGear') -> 'Iterable[_2874.BevelDifferentialPlanetGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelDifferentialPlanetGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2874.BevelDifferentialPlanetGearCompoundGearWhineAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2009.BevelDifferentialSunGear') -> 'Iterable[_2875.BevelDifferentialSunGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelDifferentialSunGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2875.BevelDifferentialSunGearCompoundGearWhineAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2001.BevelGear') -> 'Iterable[_2876.BevelGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2876.BevelGearCompoundGearWhineAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_1980.BevelGearSet') -> 'Iterable[_2877.BevelGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2877.BevelGearSetCompoundGearWhineAnalysis))

    def results_for_conical_gear(self, design_entity: '_1995.ConicalGear') -> 'Iterable[_2878.ConicalGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConicalGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2878.ConicalGearCompoundGearWhineAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_1969.ConicalGearSet') -> 'Iterable[_2879.ConicalGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConicalGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2879.ConicalGearSetCompoundGearWhineAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_1996.CylindricalGear') -> 'Iterable[_2880.CylindricalGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CylindricalGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2880.CylindricalGearCompoundGearWhineAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_1968.CylindricalGearSet') -> 'Iterable[_2881.CylindricalGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CylindricalGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2881.CylindricalGearSetCompoundGearWhineAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2014.CylindricalPlanetGear') -> 'Iterable[_2882.CylindricalPlanetGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CylindricalPlanetGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2882.CylindricalPlanetGearCompoundGearWhineAnalysis))

    def results_for_gear(self, design_entity: '_1992.Gear') -> 'Iterable[_2883.GearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.GearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2883.GearCompoundGearWhineAnalysis))

    def results_for_gear_set(self, design_entity: '_1972.GearSet') -> 'Iterable[_2884.GearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.GearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2884.GearSetCompoundGearWhineAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2002.HypoidGear') -> 'Iterable[_2885.HypoidGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.HypoidGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2885.HypoidGearCompoundGearWhineAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_1965.HypoidGearSet') -> 'Iterable[_2886.HypoidGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.HypoidGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2886.HypoidGearSetCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2000.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_2887.KlingelnbergCycloPalloidConicalGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2887.KlingelnbergCycloPalloidConicalGearCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_1971.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_2888.KlingelnbergCycloPalloidConicalGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2888.KlingelnbergCycloPalloidConicalGearSetCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2012.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_2889.KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2889.KlingelnbergCycloPalloidHypoidGearCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_1984.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_2890.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2890.KlingelnbergCycloPalloidHypoidGearSetCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2013.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_2891.KlingelnbergCycloPalloidSpiralBevelGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2891.KlingelnbergCycloPalloidSpiralBevelGearCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_2892.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2892.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundGearWhineAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_1986.PlanetaryGearSet') -> 'Iterable[_2893.PlanetaryGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PlanetaryGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2893.PlanetaryGearSetCompoundGearWhineAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2004.SpiralBevelGear') -> 'Iterable[_2894.SpiralBevelGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpiralBevelGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2894.SpiralBevelGearCompoundGearWhineAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_1966.SpiralBevelGearSet') -> 'Iterable[_2895.SpiralBevelGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpiralBevelGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2895.SpiralBevelGearSetCompoundGearWhineAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2005.StraightBevelDiffGear') -> 'Iterable[_2896.StraightBevelDiffGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelDiffGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2896.StraightBevelDiffGearCompoundGearWhineAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_1982.StraightBevelDiffGearSet') -> 'Iterable[_2897.StraightBevelDiffGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelDiffGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2897.StraightBevelDiffGearSetCompoundGearWhineAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2006.StraightBevelGear') -> 'Iterable[_2898.StraightBevelGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2898.StraightBevelGearCompoundGearWhineAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_1964.StraightBevelGearSet') -> 'Iterable[_2899.StraightBevelGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2899.StraightBevelGearSetCompoundGearWhineAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2010.StraightBevelPlanetGear') -> 'Iterable[_2900.StraightBevelPlanetGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelPlanetGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2900.StraightBevelPlanetGearCompoundGearWhineAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2011.StraightBevelSunGear') -> 'Iterable[_2901.StraightBevelSunGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelSunGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2901.StraightBevelSunGearCompoundGearWhineAnalysis))

    def results_for_worm_gear(self, design_entity: '_1998.WormGear') -> 'Iterable[_2902.WormGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.WormGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2902.WormGearCompoundGearWhineAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_1970.WormGearSet') -> 'Iterable[_2903.WormGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.WormGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2903.WormGearSetCompoundGearWhineAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2007.ZerolBevelGear') -> 'Iterable[_2904.ZerolBevelGearCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ZerolBevelGearCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2904.ZerolBevelGearCompoundGearWhineAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_1983.ZerolBevelGearSet') -> 'Iterable[_2905.ZerolBevelGearSetCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ZerolBevelGearSetCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2905.ZerolBevelGearSetCompoundGearWhineAnalysis))

    def results_for_belt_drive(self, design_entity: '_1973.BeltDrive') -> 'Iterable[_2906.BeltDriveCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BeltDriveCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2906.BeltDriveCompoundGearWhineAnalysis))

    def results_for_clutch(self, design_entity: '_1988.Clutch') -> 'Iterable[_2907.ClutchCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ClutchCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2907.ClutchCompoundGearWhineAnalysis))

    def results_for_clutch_half(self, design_entity: '_2015.ClutchHalf') -> 'Iterable[_2908.ClutchHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ClutchHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2908.ClutchHalfCompoundGearWhineAnalysis))

    def results_for_concept_coupling(self, design_entity: '_1989.ConceptCoupling') -> 'Iterable[_2909.ConceptCouplingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptCouplingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2909.ConceptCouplingCompoundGearWhineAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2016.ConceptCouplingHalf') -> 'Iterable[_2910.ConceptCouplingHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptCouplingHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2910.ConceptCouplingHalfCompoundGearWhineAnalysis))

    def results_for_coupling(self, design_entity: '_1974.Coupling') -> 'Iterable[_2911.CouplingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CouplingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2911.CouplingCompoundGearWhineAnalysis))

    def results_for_coupling_half(self, design_entity: '_1993.CouplingHalf') -> 'Iterable[_2912.CouplingHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CouplingHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2912.CouplingHalfCompoundGearWhineAnalysis))

    def results_for_cvt(self, design_entity: '_1987.CVT') -> 'Iterable[_2913.CVTCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CVTCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2913.CVTCompoundGearWhineAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2023.CVTPulley') -> 'Iterable[_2914.CVTPulleyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CVTPulleyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2914.CVTPulleyCompoundGearWhineAnalysis))

    def results_for_pulley(self, design_entity: '_2017.Pulley') -> 'Iterable[_2915.PulleyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PulleyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2915.PulleyCompoundGearWhineAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_1967.ShaftHubConnection') -> 'Iterable[_2916.ShaftHubConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ShaftHubConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2916.ShaftHubConnectionCompoundGearWhineAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2018.RollingRing') -> 'Iterable[_2917.RollingRingCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.RollingRingCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2917.RollingRingCompoundGearWhineAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_1975.RollingRingAssembly') -> 'Iterable[_2918.RollingRingAssemblyCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.RollingRingAssemblyCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2918.RollingRingAssemblyCompoundGearWhineAnalysis))

    def results_for_spring_damper(self, design_entity: '_1990.SpringDamper') -> 'Iterable[_2919.SpringDamperCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpringDamperCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2919.SpringDamperCompoundGearWhineAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2019.SpringDamperHalf') -> 'Iterable[_2920.SpringDamperHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpringDamperHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2920.SpringDamperHalfCompoundGearWhineAnalysis))

    def results_for_synchroniser(self, design_entity: '_1976.Synchroniser') -> 'Iterable[_2921.SynchroniserCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SynchroniserCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2921.SynchroniserCompoundGearWhineAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2024.SynchroniserHalf') -> 'Iterable[_2922.SynchroniserHalfCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SynchroniserHalfCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2922.SynchroniserHalfCompoundGearWhineAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2020.SynchroniserPart') -> 'Iterable[_2923.SynchroniserPartCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SynchroniserPartCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2923.SynchroniserPartCompoundGearWhineAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2025.SynchroniserSleeve') -> 'Iterable[_2924.SynchroniserSleeveCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SynchroniserSleeveCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2924.SynchroniserSleeveCompoundGearWhineAnalysis))

    def results_for_torque_converter(self, design_entity: '_1991.TorqueConverter') -> 'Iterable[_2925.TorqueConverterCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.TorqueConverterCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2925.TorqueConverterCompoundGearWhineAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2021.TorqueConverterPump') -> 'Iterable[_2926.TorqueConverterPumpCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.TorqueConverterPumpCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2926.TorqueConverterPumpCompoundGearWhineAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2022.TorqueConverterTurbine') -> 'Iterable[_2927.TorqueConverterTurbineCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.TorqueConverterTurbineCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2927.TorqueConverterTurbineCompoundGearWhineAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1765.CVTBeltConnection') -> 'Iterable[_2928.CVTBeltConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CVTBeltConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2928.CVTBeltConnectionCompoundGearWhineAnalysis))

    def results_for_belt_connection(self, design_entity: '_1760.BeltConnection') -> 'Iterable[_2929.BeltConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BeltConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2929.BeltConnectionCompoundGearWhineAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1761.CoaxialConnection') -> 'Iterable[_2930.CoaxialConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CoaxialConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2930.CoaxialConnectionCompoundGearWhineAnalysis))

    def results_for_connection(self, design_entity: '_1764.Connection') -> 'Iterable[_2931.ConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2931.ConnectionCompoundGearWhineAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1773.InterMountableComponentConnection') -> 'Iterable[_2932.InterMountableComponentConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.InterMountableComponentConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2932.InterMountableComponentConnectionCompoundGearWhineAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1776.PlanetaryConnection') -> 'Iterable[_2933.PlanetaryConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.PlanetaryConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2933.PlanetaryConnectionCompoundGearWhineAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1780.RollingRingConnection') -> 'Iterable[_2934.RollingRingConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.RollingRingConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2934.RollingRingConnectionCompoundGearWhineAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1784.ShaftToMountableComponentConnection') -> 'Iterable[_2935.ShaftToMountableComponentConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ShaftToMountableComponentConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2935.ShaftToMountableComponentConnectionCompoundGearWhineAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1822.ClutchConnection') -> 'Iterable[_2936.ClutchConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ClutchConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2936.ClutchConnectionCompoundGearWhineAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1824.ConceptCouplingConnection') -> 'Iterable[_2937.ConceptCouplingConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptCouplingConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2937.ConceptCouplingConnectionCompoundGearWhineAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1826.CouplingConnection') -> 'Iterable[_2938.CouplingConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CouplingConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2938.CouplingConnectionCompoundGearWhineAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1828.SpringDamperConnection') -> 'Iterable[_2939.SpringDamperConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpringDamperConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2939.SpringDamperConnectionCompoundGearWhineAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1830.TorqueConverterConnection') -> 'Iterable[_2940.TorqueConverterConnectionCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.TorqueConverterConnectionCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2940.TorqueConverterConnectionCompoundGearWhineAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1790.BevelDifferentialGearMesh') -> 'Iterable[_2941.BevelDifferentialGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelDifferentialGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2941.BevelDifferentialGearMeshCompoundGearWhineAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1794.ConceptGearMesh') -> 'Iterable[_2942.ConceptGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConceptGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2942.ConceptGearMeshCompoundGearWhineAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1800.FaceGearMesh') -> 'Iterable[_2943.FaceGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.FaceGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2943.FaceGearMeshCompoundGearWhineAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1814.StraightBevelDiffGearMesh') -> 'Iterable[_2944.StraightBevelDiffGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelDiffGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2944.StraightBevelDiffGearMeshCompoundGearWhineAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1792.BevelGearMesh') -> 'Iterable[_2945.BevelGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.BevelGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2945.BevelGearMeshCompoundGearWhineAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1796.ConicalGearMesh') -> 'Iterable[_2946.ConicalGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ConicalGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2946.ConicalGearMeshCompoundGearWhineAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1788.AGMAGleasonConicalGearMesh') -> 'Iterable[_2947.AGMAGleasonConicalGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.AGMAGleasonConicalGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2947.AGMAGleasonConicalGearMeshCompoundGearWhineAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1798.CylindricalGearMesh') -> 'Iterable[_2948.CylindricalGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.CylindricalGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2948.CylindricalGearMeshCompoundGearWhineAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1804.HypoidGearMesh') -> 'Iterable[_2949.HypoidGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.HypoidGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2949.HypoidGearMeshCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1807.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_2950.KlingelnbergCycloPalloidConicalGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2950.KlingelnbergCycloPalloidConicalGearMeshCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1808.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_2951.KlingelnbergCycloPalloidHypoidGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2951.KlingelnbergCycloPalloidHypoidGearMeshCompoundGearWhineAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_2952.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2952.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundGearWhineAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1812.SpiralBevelGearMesh') -> 'Iterable[_2953.SpiralBevelGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.SpiralBevelGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2953.SpiralBevelGearMeshCompoundGearWhineAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1816.StraightBevelGearMesh') -> 'Iterable[_2954.StraightBevelGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.StraightBevelGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2954.StraightBevelGearMeshCompoundGearWhineAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1818.WormGearMesh') -> 'Iterable[_2955.WormGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.WormGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2955.WormGearMeshCompoundGearWhineAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1820.ZerolBevelGearMesh') -> 'Iterable[_2956.ZerolBevelGearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.ZerolBevelGearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2956.ZerolBevelGearMeshCompoundGearWhineAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1802.GearMesh') -> 'Iterable[_2957.GearMeshCompoundGearWhineAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.gear_whine_analyses.compound.GearMeshCompoundGearWhineAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2957.GearMeshCompoundGearWhineAnalysis))
