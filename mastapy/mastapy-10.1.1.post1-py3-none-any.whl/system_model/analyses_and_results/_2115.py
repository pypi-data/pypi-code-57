'''_2115.py

CompoundDynamicAnalysisAnalysis
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
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import (
    _2656, _2657, _2658, _2659,
    _2660, _2661, _2662, _2663,
    _2664, _2665, _2666, _2667,
    _2668, _2669, _2670, _2671,
    _2672, _2673, _2674, _2675,
    _2676, _2677, _2678, _2679,
    _2680, _2681, _2682, _2683,
    _2684, _2685, _2686, _2687,
    _2688, _2689, _2690, _2691,
    _2692, _2693, _2694, _2695,
    _2696, _2697, _2698, _2699,
    _2700, _2701, _2702, _2703,
    _2704, _2705, _2706, _2707,
    _2708, _2709, _2710, _2711,
    _2712, _2713, _2714, _2715,
    _2716, _2717, _2718, _2719,
    _2720, _2721, _2722, _2723,
    _2724, _2725, _2726, _2727,
    _2728, _2729, _2730, _2731,
    _2732, _2733, _2734, _2735,
    _2736, _2737, _2738, _2739,
    _2740, _2741, _2742, _2743,
    _2744, _2745, _2746, _2747,
    _2748, _2749, _2750, _2751,
    _2752, _2753, _2754, _2755,
    _2756, _2757, _2758, _2759,
    _2760, _2761, _2762, _2763,
    _2764, _2765, _2766, _2767,
    _2768, _2769, _2770, _2771,
    _2772, _2773
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

_COMPOUND_DYNAMIC_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundDynamicAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundDynamicAnalysisAnalysis',)


class CompoundDynamicAnalysisAnalysis(_2080.CompoundAnalysis):
    '''CompoundDynamicAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_DYNAMIC_ANALYSIS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundDynamicAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1905.AbstractAssembly') -> 'Iterable[_2656.AbstractAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AbstractAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2656.AbstractAssemblyCompoundDynamicAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1906.AbstractShaftOrHousing') -> 'Iterable[_2657.AbstractShaftOrHousingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AbstractShaftOrHousingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2657.AbstractShaftOrHousingCompoundDynamicAnalysis))

    def results_for_bearing(self, design_entity: '_1908.Bearing') -> 'Iterable[_2658.BearingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BearingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2658.BearingCompoundDynamicAnalysis))

    def results_for_bolt(self, design_entity: '_1910.Bolt') -> 'Iterable[_2659.BoltCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BoltCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2659.BoltCompoundDynamicAnalysis))

    def results_for_bolted_joint(self, design_entity: '_1911.BoltedJoint') -> 'Iterable[_2660.BoltedJointCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BoltedJointCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2660.BoltedJointCompoundDynamicAnalysis))

    def results_for_component(self, design_entity: '_1912.Component') -> 'Iterable[_2661.ComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2661.ComponentCompoundDynamicAnalysis))

    def results_for_connector(self, design_entity: '_1915.Connector') -> 'Iterable[_2662.ConnectorCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConnectorCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2662.ConnectorCompoundDynamicAnalysis))

    def results_for_datum(self, design_entity: '_1916.Datum') -> 'Iterable[_2663.DatumCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.DatumCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2663.DatumCompoundDynamicAnalysis))

    def results_for_external_cad_model(self, design_entity: '_1919.ExternalCADModel') -> 'Iterable[_2664.ExternalCADModelCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ExternalCADModelCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2664.ExternalCADModelCompoundDynamicAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_1920.FlexiblePinAssembly') -> 'Iterable[_2665.FlexiblePinAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FlexiblePinAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2665.FlexiblePinAssemblyCompoundDynamicAnalysis))

    def results_for_assembly(self, design_entity: '_1904.Assembly') -> 'Iterable[_2666.AssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2666.AssemblyCompoundDynamicAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_1921.GuideDxfModel') -> 'Iterable[_2667.GuideDxfModelCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GuideDxfModelCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2667.GuideDxfModelCompoundDynamicAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_1924.ImportedFEComponent') -> 'Iterable[_2668.ImportedFEComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ImportedFEComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2668.ImportedFEComponentCompoundDynamicAnalysis))

    def results_for_mass_disc(self, design_entity: '_1926.MassDisc') -> 'Iterable[_2669.MassDiscCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MassDiscCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2669.MassDiscCompoundDynamicAnalysis))

    def results_for_measurement_component(self, design_entity: '_1927.MeasurementComponent') -> 'Iterable[_2670.MeasurementComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MeasurementComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2670.MeasurementComponentCompoundDynamicAnalysis))

    def results_for_mountable_component(self, design_entity: '_1928.MountableComponent') -> 'Iterable[_2671.MountableComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MountableComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2671.MountableComponentCompoundDynamicAnalysis))

    def results_for_oil_seal(self, design_entity: '_1929.OilSeal') -> 'Iterable[_2672.OilSealCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.OilSealCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2672.OilSealCompoundDynamicAnalysis))

    def results_for_part(self, design_entity: '_1931.Part') -> 'Iterable[_2673.PartCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2673.PartCompoundDynamicAnalysis))

    def results_for_planet_carrier(self, design_entity: '_1932.PlanetCarrier') -> 'Iterable[_2674.PlanetCarrierCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetCarrierCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2674.PlanetCarrierCompoundDynamicAnalysis))

    def results_for_point_load(self, design_entity: '_1933.PointLoad') -> 'Iterable[_2675.PointLoadCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PointLoadCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2675.PointLoadCompoundDynamicAnalysis))

    def results_for_power_load(self, design_entity: '_1934.PowerLoad') -> 'Iterable[_2676.PowerLoadCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PowerLoadCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2676.PowerLoadCompoundDynamicAnalysis))

    def results_for_root_assembly(self, design_entity: '_1935.RootAssembly') -> 'Iterable[_2677.RootAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RootAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2677.RootAssemblyCompoundDynamicAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_1937.SpecialisedAssembly') -> 'Iterable[_2678.SpecialisedAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpecialisedAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2678.SpecialisedAssemblyCompoundDynamicAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_1938.UnbalancedMass') -> 'Iterable[_2679.UnbalancedMassCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.UnbalancedMassCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2679.UnbalancedMassCompoundDynamicAnalysis))

    def results_for_virtual_component(self, design_entity: '_1939.VirtualComponent') -> 'Iterable[_2680.VirtualComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.VirtualComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2680.VirtualComponentCompoundDynamicAnalysis))

    def results_for_shaft(self, design_entity: '_1942.Shaft') -> 'Iterable[_2681.ShaftCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2681.ShaftCompoundDynamicAnalysis))

    def results_for_concept_gear(self, design_entity: '_1994.ConceptGear') -> 'Iterable[_2682.ConceptGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2682.ConceptGearCompoundDynamicAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_1977.ConceptGearSet') -> 'Iterable[_2683.ConceptGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2683.ConceptGearSetCompoundDynamicAnalysis))

    def results_for_face_gear(self, design_entity: '_1997.FaceGear') -> 'Iterable[_2684.FaceGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2684.FaceGearCompoundDynamicAnalysis))

    def results_for_face_gear_set(self, design_entity: '_1978.FaceGearSet') -> 'Iterable[_2685.FaceGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2685.FaceGearSetCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_1999.AGMAGleasonConicalGear') -> 'Iterable[_2686.AGMAGleasonConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2686.AGMAGleasonConicalGearCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_1979.AGMAGleasonConicalGearSet') -> 'Iterable[_2687.AGMAGleasonConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2687.AGMAGleasonConicalGearSetCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2003.BevelDifferentialGear') -> 'Iterable[_2688.BevelDifferentialGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2688.BevelDifferentialGearCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_1981.BevelDifferentialGearSet') -> 'Iterable[_2689.BevelDifferentialGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2689.BevelDifferentialGearSetCompoundDynamicAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2008.BevelDifferentialPlanetGear') -> 'Iterable[_2690.BevelDifferentialPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2690.BevelDifferentialPlanetGearCompoundDynamicAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2009.BevelDifferentialSunGear') -> 'Iterable[_2691.BevelDifferentialSunGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialSunGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2691.BevelDifferentialSunGearCompoundDynamicAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2001.BevelGear') -> 'Iterable[_2692.BevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2692.BevelGearCompoundDynamicAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_1980.BevelGearSet') -> 'Iterable[_2693.BevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2693.BevelGearSetCompoundDynamicAnalysis))

    def results_for_conical_gear(self, design_entity: '_1995.ConicalGear') -> 'Iterable[_2694.ConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2694.ConicalGearCompoundDynamicAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_1969.ConicalGearSet') -> 'Iterable[_2695.ConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2695.ConicalGearSetCompoundDynamicAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_1996.CylindricalGear') -> 'Iterable[_2696.CylindricalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2696.CylindricalGearCompoundDynamicAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_1968.CylindricalGearSet') -> 'Iterable[_2697.CylindricalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2697.CylindricalGearSetCompoundDynamicAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2014.CylindricalPlanetGear') -> 'Iterable[_2698.CylindricalPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2698.CylindricalPlanetGearCompoundDynamicAnalysis))

    def results_for_gear(self, design_entity: '_1992.Gear') -> 'Iterable[_2699.GearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2699.GearCompoundDynamicAnalysis))

    def results_for_gear_set(self, design_entity: '_1972.GearSet') -> 'Iterable[_2700.GearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2700.GearSetCompoundDynamicAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2002.HypoidGear') -> 'Iterable[_2701.HypoidGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2701.HypoidGearCompoundDynamicAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_1965.HypoidGearSet') -> 'Iterable[_2702.HypoidGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2702.HypoidGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2000.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_2703.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2703.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_1971.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_2704.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2704.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2012.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_2705.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2705.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_1984.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_2706.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2706.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2013.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_2707.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2707.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_2708.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2708.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_1986.PlanetaryGearSet') -> 'Iterable[_2709.PlanetaryGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetaryGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2709.PlanetaryGearSetCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2004.SpiralBevelGear') -> 'Iterable[_2710.SpiralBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2710.SpiralBevelGearCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_1966.SpiralBevelGearSet') -> 'Iterable[_2711.SpiralBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2711.SpiralBevelGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2005.StraightBevelDiffGear') -> 'Iterable[_2712.StraightBevelDiffGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2712.StraightBevelDiffGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_1982.StraightBevelDiffGearSet') -> 'Iterable[_2713.StraightBevelDiffGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2713.StraightBevelDiffGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2006.StraightBevelGear') -> 'Iterable[_2714.StraightBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2714.StraightBevelGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_1964.StraightBevelGearSet') -> 'Iterable[_2715.StraightBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2715.StraightBevelGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2010.StraightBevelPlanetGear') -> 'Iterable[_2716.StraightBevelPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2716.StraightBevelPlanetGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2011.StraightBevelSunGear') -> 'Iterable[_2717.StraightBevelSunGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelSunGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2717.StraightBevelSunGearCompoundDynamicAnalysis))

    def results_for_worm_gear(self, design_entity: '_1998.WormGear') -> 'Iterable[_2718.WormGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2718.WormGearCompoundDynamicAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_1970.WormGearSet') -> 'Iterable[_2719.WormGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2719.WormGearSetCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2007.ZerolBevelGear') -> 'Iterable[_2720.ZerolBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2720.ZerolBevelGearCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_1983.ZerolBevelGearSet') -> 'Iterable[_2721.ZerolBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2721.ZerolBevelGearSetCompoundDynamicAnalysis))

    def results_for_belt_drive(self, design_entity: '_1973.BeltDrive') -> 'Iterable[_2722.BeltDriveCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BeltDriveCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2722.BeltDriveCompoundDynamicAnalysis))

    def results_for_clutch(self, design_entity: '_1988.Clutch') -> 'Iterable[_2723.ClutchCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2723.ClutchCompoundDynamicAnalysis))

    def results_for_clutch_half(self, design_entity: '_2015.ClutchHalf') -> 'Iterable[_2724.ClutchHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2724.ClutchHalfCompoundDynamicAnalysis))

    def results_for_concept_coupling(self, design_entity: '_1989.ConceptCoupling') -> 'Iterable[_2725.ConceptCouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2725.ConceptCouplingCompoundDynamicAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2016.ConceptCouplingHalf') -> 'Iterable[_2726.ConceptCouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2726.ConceptCouplingHalfCompoundDynamicAnalysis))

    def results_for_coupling(self, design_entity: '_1974.Coupling') -> 'Iterable[_2727.CouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2727.CouplingCompoundDynamicAnalysis))

    def results_for_coupling_half(self, design_entity: '_1993.CouplingHalf') -> 'Iterable[_2728.CouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2728.CouplingHalfCompoundDynamicAnalysis))

    def results_for_cvt(self, design_entity: '_1987.CVT') -> 'Iterable[_2729.CVTCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2729.CVTCompoundDynamicAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2023.CVTPulley') -> 'Iterable[_2730.CVTPulleyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTPulleyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2730.CVTPulleyCompoundDynamicAnalysis))

    def results_for_pulley(self, design_entity: '_2017.Pulley') -> 'Iterable[_2731.PulleyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PulleyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2731.PulleyCompoundDynamicAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_1967.ShaftHubConnection') -> 'Iterable[_2732.ShaftHubConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftHubConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2732.ShaftHubConnectionCompoundDynamicAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2018.RollingRing') -> 'Iterable[_2733.RollingRingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2733.RollingRingCompoundDynamicAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_1975.RollingRingAssembly') -> 'Iterable[_2734.RollingRingAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2734.RollingRingAssemblyCompoundDynamicAnalysis))

    def results_for_spring_damper(self, design_entity: '_1990.SpringDamper') -> 'Iterable[_2735.SpringDamperCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2735.SpringDamperCompoundDynamicAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2019.SpringDamperHalf') -> 'Iterable[_2736.SpringDamperHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2736.SpringDamperHalfCompoundDynamicAnalysis))

    def results_for_synchroniser(self, design_entity: '_1976.Synchroniser') -> 'Iterable[_2737.SynchroniserCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2737.SynchroniserCompoundDynamicAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2024.SynchroniserHalf') -> 'Iterable[_2738.SynchroniserHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2738.SynchroniserHalfCompoundDynamicAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2020.SynchroniserPart') -> 'Iterable[_2739.SynchroniserPartCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserPartCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2739.SynchroniserPartCompoundDynamicAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2025.SynchroniserSleeve') -> 'Iterable[_2740.SynchroniserSleeveCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserSleeveCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2740.SynchroniserSleeveCompoundDynamicAnalysis))

    def results_for_torque_converter(self, design_entity: '_1991.TorqueConverter') -> 'Iterable[_2741.TorqueConverterCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2741.TorqueConverterCompoundDynamicAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2021.TorqueConverterPump') -> 'Iterable[_2742.TorqueConverterPumpCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterPumpCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2742.TorqueConverterPumpCompoundDynamicAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2022.TorqueConverterTurbine') -> 'Iterable[_2743.TorqueConverterTurbineCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterTurbineCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2743.TorqueConverterTurbineCompoundDynamicAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1765.CVTBeltConnection') -> 'Iterable[_2744.CVTBeltConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTBeltConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2744.CVTBeltConnectionCompoundDynamicAnalysis))

    def results_for_belt_connection(self, design_entity: '_1760.BeltConnection') -> 'Iterable[_2745.BeltConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BeltConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2745.BeltConnectionCompoundDynamicAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1761.CoaxialConnection') -> 'Iterable[_2746.CoaxialConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CoaxialConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2746.CoaxialConnectionCompoundDynamicAnalysis))

    def results_for_connection(self, design_entity: '_1764.Connection') -> 'Iterable[_2747.ConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2747.ConnectionCompoundDynamicAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1773.InterMountableComponentConnection') -> 'Iterable[_2748.InterMountableComponentConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.InterMountableComponentConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2748.InterMountableComponentConnectionCompoundDynamicAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1776.PlanetaryConnection') -> 'Iterable[_2749.PlanetaryConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetaryConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2749.PlanetaryConnectionCompoundDynamicAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1780.RollingRingConnection') -> 'Iterable[_2750.RollingRingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2750.RollingRingConnectionCompoundDynamicAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1784.ShaftToMountableComponentConnection') -> 'Iterable[_2751.ShaftToMountableComponentConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftToMountableComponentConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2751.ShaftToMountableComponentConnectionCompoundDynamicAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1822.ClutchConnection') -> 'Iterable[_2752.ClutchConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2752.ClutchConnectionCompoundDynamicAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1824.ConceptCouplingConnection') -> 'Iterable[_2753.ConceptCouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2753.ConceptCouplingConnectionCompoundDynamicAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1826.CouplingConnection') -> 'Iterable[_2754.CouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2754.CouplingConnectionCompoundDynamicAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1828.SpringDamperConnection') -> 'Iterable[_2755.SpringDamperConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2755.SpringDamperConnectionCompoundDynamicAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1830.TorqueConverterConnection') -> 'Iterable[_2756.TorqueConverterConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2756.TorqueConverterConnectionCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1790.BevelDifferentialGearMesh') -> 'Iterable[_2757.BevelDifferentialGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2757.BevelDifferentialGearMeshCompoundDynamicAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1794.ConceptGearMesh') -> 'Iterable[_2758.ConceptGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2758.ConceptGearMeshCompoundDynamicAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1800.FaceGearMesh') -> 'Iterable[_2759.FaceGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2759.FaceGearMeshCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1814.StraightBevelDiffGearMesh') -> 'Iterable[_2760.StraightBevelDiffGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2760.StraightBevelDiffGearMeshCompoundDynamicAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1792.BevelGearMesh') -> 'Iterable[_2761.BevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2761.BevelGearMeshCompoundDynamicAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1796.ConicalGearMesh') -> 'Iterable[_2762.ConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2762.ConicalGearMeshCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1788.AGMAGleasonConicalGearMesh') -> 'Iterable[_2763.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2763.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1798.CylindricalGearMesh') -> 'Iterable[_2764.CylindricalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2764.CylindricalGearMeshCompoundDynamicAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1804.HypoidGearMesh') -> 'Iterable[_2765.HypoidGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2765.HypoidGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1807.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_2766.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2766.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1808.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_2767.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2767.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_2768.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2768.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1812.SpiralBevelGearMesh') -> 'Iterable[_2769.SpiralBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2769.SpiralBevelGearMeshCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1816.StraightBevelGearMesh') -> 'Iterable[_2770.StraightBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2770.StraightBevelGearMeshCompoundDynamicAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1818.WormGearMesh') -> 'Iterable[_2771.WormGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2771.WormGearMeshCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1820.ZerolBevelGearMesh') -> 'Iterable[_2772.ZerolBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2772.ZerolBevelGearMeshCompoundDynamicAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1802.GearMesh') -> 'Iterable[_2773.GearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_2773.GearMeshCompoundDynamicAnalysis))
