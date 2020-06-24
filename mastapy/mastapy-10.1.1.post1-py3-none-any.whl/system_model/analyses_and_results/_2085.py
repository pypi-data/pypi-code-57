'''_2085.py

DynamicAnalysisAnalysis
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _2166, _2169, _2171, _2172,
    _2173, _2174, _2175, _2176,
    _2178, _2180, _2182, _2184,
    _2186, _2188, _2190, _2192,
    _2194, _2196, _2198, _2200,
    _2202, _2204, _2206, _2208,
    _2210, _2212, _2213, _2214,
    _2216, _2218, _2220, _2222,
    _2224, _2225, _2226, _2228,
    _2230, _2232, _2233, _2234,
    _2236, _2238, _2239, _2241,
    _2242, _2244, _2246, _2248,
    _2250, _2252, _2254, _2256,
    _2258, _2260, _2262, _2263,
    _2264, _2265, _2266, _2267,
    _2268, _2270, _2272, _2274,
    _2276, _2277, _2279, _2281,
    _2283, _2285, _2287, _2289,
    _2291, _2293, _2295, _2297,
    _2299, _2301, _2303, _2305,
    _2306, _2307, _2308, _2310,
    _2312, _2313, _2314, _2315,
    _2316, _2317, _2318, _2319,
    _2320, _2322, _2324, _2326,
    _2328, _2330, _2332, _2334,
    _2336, _2338, _2340, _2342,
    _2344, _2346, _2348, _2350,
    _2351, _2353, _2355, _2357,
    _2359, _2361, _2363, _2365,
    _2367, _2369
)
from mastapy.system_model.analyses_and_results.dynamic_analyses import (
    _3618, _3619, _3620, _3621,
    _3622, _3623, _3624, _3625,
    _3626, _3627, _3628, _3629,
    _3630, _3631, _3632, _3633,
    _3634, _3635, _3636, _3637,
    _3638, _3639, _3640, _3641,
    _3642, _3643, _3644, _3645,
    _3646, _3647, _3648, _3649,
    _3650, _3651, _3652, _3653,
    _3654, _3655, _3656, _3657,
    _3658, _3659, _3660, _3661,
    _3662, _3663, _3664, _3665,
    _3666, _3667, _3668, _3669,
    _3670, _3671, _3672, _3673,
    _3674, _3675, _3676, _3677,
    _3678, _3679, _3680, _3681,
    _3682, _3683, _3684, _3685,
    _3686, _3687, _3688, _3689,
    _3690, _3691, _3692, _3693,
    _3694, _3695, _3696, _3697,
    _3698, _3699, _3700, _3701,
    _3702, _3703, _3704, _3705,
    _3706, _3707, _3708, _3709,
    _3710, _3711, _3712, _3713,
    _3714, _3715, _3716, _3717,
    _3718, _3719, _3720, _3721,
    _3722, _3723, _3724, _3725,
    _3726, _3727, _3728, _3729,
    _3730, _3731, _3732, _3733,
    _3734, _3735
)
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import (
    _2007, _1983, _1994, _1977,
    _1997, _1978, _1999, _1979,
    _2003, _1981, _2008, _2009,
    _2001, _1980, _1995, _1969,
    _1996, _1968, _2014, _1992,
    _1972, _2002, _1965, _2000,
    _1971, _2012, _1984, _2013,
    _1985, _1986, _2004, _1966,
    _2005, _1982, _2006, _1964,
    _2010, _2011, _1998, _1970
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
from mastapy.system_model.part_model import (
    _1905, _1906, _1908, _1910,
    _1911, _1912, _1915, _1916,
    _1919, _1920, _1904, _1921,
    _1924, _1926, _1927, _1928,
    _1929, _1931, _1932, _1933,
    _1934, _1935, _1937, _1938,
    _1939
)
from mastapy.system_model.part_model.shaft_model import _1942
from mastapy.system_model.analyses_and_results import _2081
from mastapy._internal.python_net import python_net_import

_DYNAMIC_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'DynamicAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicAnalysisAnalysis',)


class DynamicAnalysisAnalysis(_2081.SingleAnalysis):
    '''DynamicAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_ANALYSIS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_2166.WormGearSetLoadCase') -> '_3618.WormGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3618.WormGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2007.ZerolBevelGear') -> '_3619.ZerolBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3619.ZerolBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_2169.ZerolBevelGearLoadCase') -> '_3619.ZerolBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3619.ZerolBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_1983.ZerolBevelGearSet') -> '_3620.ZerolBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3620.ZerolBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_2171.ZerolBevelGearSetLoadCase') -> '_3620.ZerolBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3620.ZerolBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_1973.BeltDrive') -> '_3621.BeltDriveDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BeltDriveDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3621.BeltDriveDynamicAnalysis)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_2172.BeltDriveLoadCase') -> '_3621.BeltDriveDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BeltDriveDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3621.BeltDriveDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_1988.Clutch') -> '_3622.ClutchDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3622.ClutchDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_2173.ClutchLoadCase') -> '_3622.ClutchDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3622.ClutchDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2015.ClutchHalf') -> '_3623.ClutchHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3623.ClutchHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_2174.ClutchHalfLoadCase') -> '_3623.ClutchHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3623.ClutchHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_1989.ConceptCoupling') -> '_3624.ConceptCouplingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3624.ConceptCouplingDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_2175.ConceptCouplingLoadCase') -> '_3624.ConceptCouplingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3624.ConceptCouplingDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2016.ConceptCouplingHalf') -> '_3625.ConceptCouplingHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3625.ConceptCouplingHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_2176.ConceptCouplingHalfLoadCase') -> '_3625.ConceptCouplingHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3625.ConceptCouplingHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_1974.Coupling') -> '_3626.CouplingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3626.CouplingDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_2178.CouplingLoadCase') -> '_3626.CouplingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3626.CouplingDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_1993.CouplingHalf') -> '_3627.CouplingHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3627.CouplingHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_2180.CouplingHalfLoadCase') -> '_3627.CouplingHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3627.CouplingHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_1987.CVT') -> '_3628.CVTDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3628.CVTDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_2182.CVTLoadCase') -> '_3628.CVTDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3628.CVTDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2023.CVTPulley') -> '_3629.CVTPulleyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTPulleyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3629.CVTPulleyDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_2184.CVTPulleyLoadCase') -> '_3629.CVTPulleyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTPulleyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3629.CVTPulleyDynamicAnalysis)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2017.Pulley') -> '_3630.PulleyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PulleyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3630.PulleyDynamicAnalysis)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_2186.PulleyLoadCase') -> '_3630.PulleyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PulleyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3630.PulleyDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_1967.ShaftHubConnection') -> '_3631.ShaftHubConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftHubConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3631.ShaftHubConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_2188.ShaftHubConnectionLoadCase') -> '_3631.ShaftHubConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftHubConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3631.ShaftHubConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2018.RollingRing') -> '_3632.RollingRingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3632.RollingRingDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_2190.RollingRingLoadCase') -> '_3632.RollingRingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3632.RollingRingDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_1975.RollingRingAssembly') -> '_3633.RollingRingAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3633.RollingRingAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_2192.RollingRingAssemblyLoadCase') -> '_3633.RollingRingAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3633.RollingRingAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_1990.SpringDamper') -> '_3634.SpringDamperDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3634.SpringDamperDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_2194.SpringDamperLoadCase') -> '_3634.SpringDamperDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3634.SpringDamperDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2019.SpringDamperHalf') -> '_3635.SpringDamperHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3635.SpringDamperHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_2196.SpringDamperHalfLoadCase') -> '_3635.SpringDamperHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3635.SpringDamperHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_1976.Synchroniser') -> '_3636.SynchroniserDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3636.SynchroniserDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_2198.SynchroniserLoadCase') -> '_3636.SynchroniserDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3636.SynchroniserDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2024.SynchroniserHalf') -> '_3637.SynchroniserHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3637.SynchroniserHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_2200.SynchroniserHalfLoadCase') -> '_3637.SynchroniserHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3637.SynchroniserHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2020.SynchroniserPart') -> '_3638.SynchroniserPartDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserPartDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3638.SynchroniserPartDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_2202.SynchroniserPartLoadCase') -> '_3638.SynchroniserPartDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserPartDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3638.SynchroniserPartDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2025.SynchroniserSleeve') -> '_3639.SynchroniserSleeveDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserSleeveDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3639.SynchroniserSleeveDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_2204.SynchroniserSleeveLoadCase') -> '_3639.SynchroniserSleeveDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserSleeveDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3639.SynchroniserSleeveDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_1991.TorqueConverter') -> '_3640.TorqueConverterDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3640.TorqueConverterDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_2206.TorqueConverterLoadCase') -> '_3640.TorqueConverterDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3640.TorqueConverterDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2021.TorqueConverterPump') -> '_3641.TorqueConverterPumpDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterPumpDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3641.TorqueConverterPumpDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_2208.TorqueConverterPumpLoadCase') -> '_3641.TorqueConverterPumpDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterPumpDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3641.TorqueConverterPumpDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2022.TorqueConverterTurbine') -> '_3642.TorqueConverterTurbineDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterTurbineDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3642.TorqueConverterTurbineDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_2210.TorqueConverterTurbineLoadCase') -> '_3642.TorqueConverterTurbineDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterTurbineDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3642.TorqueConverterTurbineDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1765.CVTBeltConnection') -> '_3643.CVTBeltConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTBeltConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3643.CVTBeltConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_2212.CVTBeltConnectionLoadCase') -> '_3643.CVTBeltConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTBeltConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3643.CVTBeltConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1760.BeltConnection') -> '_3644.BeltConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BeltConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3644.BeltConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_2213.BeltConnectionLoadCase') -> '_3644.BeltConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BeltConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3644.BeltConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1761.CoaxialConnection') -> '_3645.CoaxialConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CoaxialConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3645.CoaxialConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_2214.CoaxialConnectionLoadCase') -> '_3645.CoaxialConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CoaxialConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3645.CoaxialConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1764.Connection') -> '_3646.ConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3646.ConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_2216.ConnectionLoadCase') -> '_3646.ConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3646.ConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1773.InterMountableComponentConnection') -> '_3647.InterMountableComponentConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.InterMountableComponentConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3647.InterMountableComponentConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_2218.InterMountableComponentConnectionLoadCase') -> '_3647.InterMountableComponentConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.InterMountableComponentConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3647.InterMountableComponentConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1776.PlanetaryConnection') -> '_3648.PlanetaryConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetaryConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3648.PlanetaryConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_2220.PlanetaryConnectionLoadCase') -> '_3648.PlanetaryConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetaryConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3648.PlanetaryConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1780.RollingRingConnection') -> '_3649.RollingRingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3649.RollingRingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_2222.RollingRingConnectionLoadCase') -> '_3649.RollingRingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3649.RollingRingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1784.ShaftToMountableComponentConnection') -> '_3650.ShaftToMountableComponentConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftToMountableComponentConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3650.ShaftToMountableComponentConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_2224.ShaftToMountableComponentConnectionLoadCase') -> '_3650.ShaftToMountableComponentConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftToMountableComponentConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3650.ShaftToMountableComponentConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1822.ClutchConnection') -> '_3651.ClutchConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3651.ClutchConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_2225.ClutchConnectionLoadCase') -> '_3651.ClutchConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3651.ClutchConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1824.ConceptCouplingConnection') -> '_3652.ConceptCouplingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3652.ConceptCouplingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_2226.ConceptCouplingConnectionLoadCase') -> '_3652.ConceptCouplingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3652.ConceptCouplingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1826.CouplingConnection') -> '_3653.CouplingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3653.CouplingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_2228.CouplingConnectionLoadCase') -> '_3653.CouplingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3653.CouplingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1828.SpringDamperConnection') -> '_3654.SpringDamperConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3654.SpringDamperConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_2230.SpringDamperConnectionLoadCase') -> '_3654.SpringDamperConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3654.SpringDamperConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1830.TorqueConverterConnection') -> '_3655.TorqueConverterConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3655.TorqueConverterConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_2232.TorqueConverterConnectionLoadCase') -> '_3655.TorqueConverterConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3655.TorqueConverterConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1790.BevelDifferentialGearMesh') -> '_3656.BevelDifferentialGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3656.BevelDifferentialGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_2233.BevelDifferentialGearMeshLoadCase') -> '_3656.BevelDifferentialGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3656.BevelDifferentialGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1794.ConceptGearMesh') -> '_3657.ConceptGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3657.ConceptGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_2234.ConceptGearMeshLoadCase') -> '_3657.ConceptGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3657.ConceptGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1800.FaceGearMesh') -> '_3658.FaceGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3658.FaceGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_2236.FaceGearMeshLoadCase') -> '_3658.FaceGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3658.FaceGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1814.StraightBevelDiffGearMesh') -> '_3659.StraightBevelDiffGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3659.StraightBevelDiffGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_2238.StraightBevelDiffGearMeshLoadCase') -> '_3659.StraightBevelDiffGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3659.StraightBevelDiffGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1792.BevelGearMesh') -> '_3660.BevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3660.BevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2239.BevelGearMeshLoadCase') -> '_3660.BevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3660.BevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1796.ConicalGearMesh') -> '_3661.ConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3661.ConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_2241.ConicalGearMeshLoadCase') -> '_3661.ConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3661.ConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1788.AGMAGleasonConicalGearMesh') -> '_3662.AGMAGleasonConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3662.AGMAGleasonConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_2242.AGMAGleasonConicalGearMeshLoadCase') -> '_3662.AGMAGleasonConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3662.AGMAGleasonConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1798.CylindricalGearMesh') -> '_3663.CylindricalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3663.CylindricalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_2244.CylindricalGearMeshLoadCase') -> '_3663.CylindricalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3663.CylindricalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1804.HypoidGearMesh') -> '_3664.HypoidGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3664.HypoidGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_2246.HypoidGearMeshLoadCase') -> '_3664.HypoidGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3664.HypoidGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1807.KlingelnbergCycloPalloidConicalGearMesh') -> '_3665.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3665.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_2248.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_3665.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3665.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1808.KlingelnbergCycloPalloidHypoidGearMesh') -> '_3666.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3666.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_2250.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_3666.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3666.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_3667.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3667.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2252.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_3667.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3667.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1812.SpiralBevelGearMesh') -> '_3668.SpiralBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3668.SpiralBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2254.SpiralBevelGearMeshLoadCase') -> '_3668.SpiralBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3668.SpiralBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1816.StraightBevelGearMesh') -> '_3669.StraightBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3669.StraightBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2256.StraightBevelGearMeshLoadCase') -> '_3669.StraightBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3669.StraightBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1818.WormGearMesh') -> '_3670.WormGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3670.WormGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_2258.WormGearMeshLoadCase') -> '_3670.WormGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3670.WormGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1820.ZerolBevelGearMesh') -> '_3671.ZerolBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3671.ZerolBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2260.ZerolBevelGearMeshLoadCase') -> '_3671.ZerolBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3671.ZerolBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1802.GearMesh') -> '_3672.GearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3672.GearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_2262.GearMeshLoadCase') -> '_3672.GearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3672.GearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1905.AbstractAssembly') -> '_3673.AbstractAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AbstractAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3673.AbstractAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_2263.AbstractAssemblyLoadCase') -> '_3673.AbstractAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AbstractAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3673.AbstractAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1906.AbstractShaftOrHousing') -> '_3674.AbstractShaftOrHousingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AbstractShaftOrHousingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3674.AbstractShaftOrHousingDynamicAnalysis)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_2264.AbstractShaftOrHousingLoadCase') -> '_3674.AbstractShaftOrHousingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AbstractShaftOrHousingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3674.AbstractShaftOrHousingDynamicAnalysis)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1908.Bearing') -> '_3675.BearingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BearingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3675.BearingDynamicAnalysis)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_2265.BearingLoadCase') -> '_3675.BearingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BearingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3675.BearingDynamicAnalysis)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1910.Bolt') -> '_3676.BoltDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BoltDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3676.BoltDynamicAnalysis)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_2266.BoltLoadCase') -> '_3676.BoltDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BoltDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3676.BoltDynamicAnalysis)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1911.BoltedJoint') -> '_3677.BoltedJointDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BoltedJointDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3677.BoltedJointDynamicAnalysis)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_2267.BoltedJointLoadCase') -> '_3677.BoltedJointDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BoltedJointDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3677.BoltedJointDynamicAnalysis)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1912.Component') -> '_3678.ComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3678.ComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_2268.ComponentLoadCase') -> '_3678.ComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3678.ComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1915.Connector') -> '_3679.ConnectorDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConnectorDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3679.ConnectorDynamicAnalysis)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_2270.ConnectorLoadCase') -> '_3679.ConnectorDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConnectorDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3679.ConnectorDynamicAnalysis)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1916.Datum') -> '_3680.DatumDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.DatumDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3680.DatumDynamicAnalysis)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_2272.DatumLoadCase') -> '_3680.DatumDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.DatumDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3680.DatumDynamicAnalysis)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1919.ExternalCADModel') -> '_3681.ExternalCADModelDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ExternalCADModelDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3681.ExternalCADModelDynamicAnalysis)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_2274.ExternalCADModelLoadCase') -> '_3681.ExternalCADModelDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ExternalCADModelDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3681.ExternalCADModelDynamicAnalysis)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1920.FlexiblePinAssembly') -> '_3682.FlexiblePinAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FlexiblePinAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3682.FlexiblePinAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_2276.FlexiblePinAssemblyLoadCase') -> '_3682.FlexiblePinAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FlexiblePinAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3682.FlexiblePinAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1904.Assembly') -> '_3683.AssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3683.AssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_2277.AssemblyLoadCase') -> '_3683.AssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3683.AssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1921.GuideDxfModel') -> '_3684.GuideDxfModelDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GuideDxfModelDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3684.GuideDxfModelDynamicAnalysis)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_2279.GuideDxfModelLoadCase') -> '_3684.GuideDxfModelDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GuideDxfModelDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3684.GuideDxfModelDynamicAnalysis)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1924.ImportedFEComponent') -> '_3685.ImportedFEComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ImportedFEComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3685.ImportedFEComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_2281.ImportedFEComponentLoadCase') -> '_3685.ImportedFEComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ImportedFEComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3685.ImportedFEComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_1926.MassDisc') -> '_3686.MassDiscDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MassDiscDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3686.MassDiscDynamicAnalysis)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_2283.MassDiscLoadCase') -> '_3686.MassDiscDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MassDiscDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3686.MassDiscDynamicAnalysis)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_1927.MeasurementComponent') -> '_3687.MeasurementComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MeasurementComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3687.MeasurementComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_2285.MeasurementComponentLoadCase') -> '_3687.MeasurementComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MeasurementComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3687.MeasurementComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_1928.MountableComponent') -> '_3688.MountableComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MountableComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3688.MountableComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_2287.MountableComponentLoadCase') -> '_3688.MountableComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MountableComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3688.MountableComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_1929.OilSeal') -> '_3689.OilSealDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.OilSealDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3689.OilSealDynamicAnalysis)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_2289.OilSealLoadCase') -> '_3689.OilSealDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.OilSealDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3689.OilSealDynamicAnalysis)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_1931.Part') -> '_3690.PartDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PartDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3690.PartDynamicAnalysis)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_2291.PartLoadCase') -> '_3690.PartDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PartDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3690.PartDynamicAnalysis)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_1932.PlanetCarrier') -> '_3691.PlanetCarrierDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetCarrierDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3691.PlanetCarrierDynamicAnalysis)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_2293.PlanetCarrierLoadCase') -> '_3691.PlanetCarrierDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetCarrierDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3691.PlanetCarrierDynamicAnalysis)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_1933.PointLoad') -> '_3692.PointLoadDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PointLoadDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3692.PointLoadDynamicAnalysis)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_2295.PointLoadLoadCase') -> '_3692.PointLoadDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PointLoadDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3692.PointLoadDynamicAnalysis)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_1934.PowerLoad') -> '_3693.PowerLoadDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PowerLoadDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3693.PowerLoadDynamicAnalysis)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_2297.PowerLoadLoadCase') -> '_3693.PowerLoadDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PowerLoadDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3693.PowerLoadDynamicAnalysis)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_1935.RootAssembly') -> '_3694.RootAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RootAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3694.RootAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_2299.RootAssemblyLoadCase') -> '_3694.RootAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RootAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3694.RootAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_1937.SpecialisedAssembly') -> '_3695.SpecialisedAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpecialisedAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3695.SpecialisedAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_2301.SpecialisedAssemblyLoadCase') -> '_3695.SpecialisedAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpecialisedAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3695.SpecialisedAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_1938.UnbalancedMass') -> '_3696.UnbalancedMassDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.UnbalancedMassDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3696.UnbalancedMassDynamicAnalysis)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_2303.UnbalancedMassLoadCase') -> '_3696.UnbalancedMassDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.UnbalancedMassDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3696.UnbalancedMassDynamicAnalysis)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_1939.VirtualComponent') -> '_3697.VirtualComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.VirtualComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3697.VirtualComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_2305.VirtualComponentLoadCase') -> '_3697.VirtualComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.VirtualComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3697.VirtualComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_1942.Shaft') -> '_3698.ShaftDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3698.ShaftDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_2306.ShaftLoadCase') -> '_3698.ShaftDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3698.ShaftDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_1994.ConceptGear') -> '_3699.ConceptGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3699.ConceptGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_2307.ConceptGearLoadCase') -> '_3699.ConceptGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3699.ConceptGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_1977.ConceptGearSet') -> '_3700.ConceptGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3700.ConceptGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_2308.ConceptGearSetLoadCase') -> '_3700.ConceptGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3700.ConceptGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_1997.FaceGear') -> '_3701.FaceGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3701.FaceGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_2310.FaceGearLoadCase') -> '_3701.FaceGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3701.FaceGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_1978.FaceGearSet') -> '_3702.FaceGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3702.FaceGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_2312.FaceGearSetLoadCase') -> '_3702.FaceGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3702.FaceGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_1999.AGMAGleasonConicalGear') -> '_3703.AGMAGleasonConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3703.AGMAGleasonConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_2313.AGMAGleasonConicalGearLoadCase') -> '_3703.AGMAGleasonConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3703.AGMAGleasonConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_1979.AGMAGleasonConicalGearSet') -> '_3704.AGMAGleasonConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3704.AGMAGleasonConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_2314.AGMAGleasonConicalGearSetLoadCase') -> '_3704.AGMAGleasonConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3704.AGMAGleasonConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2003.BevelDifferentialGear') -> '_3705.BevelDifferentialGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3705.BevelDifferentialGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_2315.BevelDifferentialGearLoadCase') -> '_3705.BevelDifferentialGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3705.BevelDifferentialGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_1981.BevelDifferentialGearSet') -> '_3706.BevelDifferentialGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3706.BevelDifferentialGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_2316.BevelDifferentialGearSetLoadCase') -> '_3706.BevelDifferentialGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3706.BevelDifferentialGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2008.BevelDifferentialPlanetGear') -> '_3707.BevelDifferentialPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3707.BevelDifferentialPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_2317.BevelDifferentialPlanetGearLoadCase') -> '_3707.BevelDifferentialPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3707.BevelDifferentialPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2009.BevelDifferentialSunGear') -> '_3708.BevelDifferentialSunGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialSunGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3708.BevelDifferentialSunGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_2318.BevelDifferentialSunGearLoadCase') -> '_3708.BevelDifferentialSunGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialSunGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3708.BevelDifferentialSunGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2001.BevelGear') -> '_3709.BevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3709.BevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_2319.BevelGearLoadCase') -> '_3709.BevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3709.BevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_1980.BevelGearSet') -> '_3710.BevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3710.BevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_2320.BevelGearSetLoadCase') -> '_3710.BevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3710.BevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_1995.ConicalGear') -> '_3711.ConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3711.ConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_2322.ConicalGearLoadCase') -> '_3711.ConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3711.ConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_1969.ConicalGearSet') -> '_3712.ConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3712.ConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_2324.ConicalGearSetLoadCase') -> '_3712.ConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3712.ConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_1996.CylindricalGear') -> '_3713.CylindricalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3713.CylindricalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_2326.CylindricalGearLoadCase') -> '_3713.CylindricalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3713.CylindricalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_1968.CylindricalGearSet') -> '_3714.CylindricalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3714.CylindricalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_2328.CylindricalGearSetLoadCase') -> '_3714.CylindricalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3714.CylindricalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2014.CylindricalPlanetGear') -> '_3715.CylindricalPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3715.CylindricalPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_2330.CylindricalPlanetGearLoadCase') -> '_3715.CylindricalPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3715.CylindricalPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_1992.Gear') -> '_3716.GearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3716.GearDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_2332.GearLoadCase') -> '_3716.GearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3716.GearDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_1972.GearSet') -> '_3717.GearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3717.GearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_2334.GearSetLoadCase') -> '_3717.GearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3717.GearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2002.HypoidGear') -> '_3718.HypoidGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3718.HypoidGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_2336.HypoidGearLoadCase') -> '_3718.HypoidGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3718.HypoidGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_1965.HypoidGearSet') -> '_3719.HypoidGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3719.HypoidGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_2338.HypoidGearSetLoadCase') -> '_3719.HypoidGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3719.HypoidGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2000.KlingelnbergCycloPalloidConicalGear') -> '_3720.KlingelnbergCycloPalloidConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3720.KlingelnbergCycloPalloidConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_2340.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_3720.KlingelnbergCycloPalloidConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3720.KlingelnbergCycloPalloidConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_1971.KlingelnbergCycloPalloidConicalGearSet') -> '_3721.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3721.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_2342.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_3721.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3721.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2012.KlingelnbergCycloPalloidHypoidGear') -> '_3722.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3722.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_2344.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_3722.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3722.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_1984.KlingelnbergCycloPalloidHypoidGearSet') -> '_3723.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3723.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_2346.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_3723.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3723.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2013.KlingelnbergCycloPalloidSpiralBevelGear') -> '_3724.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3724.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_2348.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_3724.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3724.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_3725.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3725.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_2350.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_3725.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3725.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_1986.PlanetaryGearSet') -> '_3726.PlanetaryGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetaryGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3726.PlanetaryGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_2351.PlanetaryGearSetLoadCase') -> '_3726.PlanetaryGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetaryGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3726.PlanetaryGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2004.SpiralBevelGear') -> '_3727.SpiralBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3727.SpiralBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_2353.SpiralBevelGearLoadCase') -> '_3727.SpiralBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3727.SpiralBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_1966.SpiralBevelGearSet') -> '_3728.SpiralBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3728.SpiralBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_2355.SpiralBevelGearSetLoadCase') -> '_3728.SpiralBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3728.SpiralBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2005.StraightBevelDiffGear') -> '_3729.StraightBevelDiffGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3729.StraightBevelDiffGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_2357.StraightBevelDiffGearLoadCase') -> '_3729.StraightBevelDiffGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3729.StraightBevelDiffGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_1982.StraightBevelDiffGearSet') -> '_3730.StraightBevelDiffGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3730.StraightBevelDiffGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_2359.StraightBevelDiffGearSetLoadCase') -> '_3730.StraightBevelDiffGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3730.StraightBevelDiffGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2006.StraightBevelGear') -> '_3731.StraightBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3731.StraightBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_2361.StraightBevelGearLoadCase') -> '_3731.StraightBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3731.StraightBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_1964.StraightBevelGearSet') -> '_3732.StraightBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3732.StraightBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_2363.StraightBevelGearSetLoadCase') -> '_3732.StraightBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3732.StraightBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2010.StraightBevelPlanetGear') -> '_3733.StraightBevelPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3733.StraightBevelPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_2365.StraightBevelPlanetGearLoadCase') -> '_3733.StraightBevelPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3733.StraightBevelPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2011.StraightBevelSunGear') -> '_3734.StraightBevelSunGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelSunGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3734.StraightBevelSunGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_2367.StraightBevelSunGearLoadCase') -> '_3734.StraightBevelSunGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelSunGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3734.StraightBevelSunGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_1998.WormGear') -> '_3735.WormGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3735.WormGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_2369.WormGearLoadCase') -> '_3735.WormGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3735.WormGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_1970.WormGearSet') -> '_3618.WormGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3618.WormGearSetDynamicAnalysis)(method_result) if method_result else None
