'''_2098.py

ParametricStudyToolAnalysis
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
from mastapy.system_model.analyses_and_results.parametric_study_tools import (
    _3975, _3976, _3977, _3978,
    _3979, _3980, _3981, _3982,
    _3983, _3984, _3985, _3986,
    _3987, _3988, _3989, _3990,
    _3991, _3992, _3993, _3994,
    _3995, _3996, _3997, _3998,
    _3999, _4000, _4001, _4002,
    _4003, _4004, _4005, _4006,
    _4007, _4008, _4009, _4010,
    _4011, _4012, _4013, _4014,
    _4015, _4016, _4017, _4018,
    _4019, _4020, _4021, _4022,
    _4023, _4024, _4025, _4026,
    _4027, _4028, _4029, _4030,
    _4031, _4032, _4033, _4034,
    _4035, _4036, _4037, _4038,
    _4039, _4040, _4041, _4042,
    _4043, _4044, _4045, _4046,
    _4047, _4048, _4049, _4050,
    _4051, _4052, _4053, _4054,
    _4055, _4056, _4057, _4058,
    _4059, _4060, _4061, _4062,
    _4063, _4064, _4065, _4066,
    _4067, _4068, _4069, _4070,
    _4071, _4072, _4073, _4074,
    _4075, _4076, _4077, _4078,
    _4079, _4080, _4081, _4082,
    _4083, _4084, _4085, _4086,
    _4087, _4088, _4089, _4090,
    _4091, _4092
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

_PARAMETRIC_STUDY_TOOL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'ParametricStudyToolAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyToolAnalysis',)


class ParametricStudyToolAnalysis(_2081.SingleAnalysis):
    '''ParametricStudyToolAnalysis

    This is a mastapy class.
    '''

    TYPE = _PARAMETRIC_STUDY_TOOL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParametricStudyToolAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_2166.WormGearSetLoadCase') -> '_3975.WormGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3975.WormGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2007.ZerolBevelGear') -> '_3976.ZerolBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3976.ZerolBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_2169.ZerolBevelGearLoadCase') -> '_3976.ZerolBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3976.ZerolBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_1983.ZerolBevelGearSet') -> '_3977.ZerolBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3977.ZerolBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_2171.ZerolBevelGearSetLoadCase') -> '_3977.ZerolBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3977.ZerolBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_1973.BeltDrive') -> '_3978.BeltDriveParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BeltDriveParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3978.BeltDriveParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_2172.BeltDriveLoadCase') -> '_3978.BeltDriveParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BeltDriveParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3978.BeltDriveParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_1988.Clutch') -> '_3979.ClutchParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3979.ClutchParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_2173.ClutchLoadCase') -> '_3979.ClutchParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3979.ClutchParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2015.ClutchHalf') -> '_3980.ClutchHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3980.ClutchHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_2174.ClutchHalfLoadCase') -> '_3980.ClutchHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3980.ClutchHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_1989.ConceptCoupling') -> '_3981.ConceptCouplingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3981.ConceptCouplingParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_2175.ConceptCouplingLoadCase') -> '_3981.ConceptCouplingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3981.ConceptCouplingParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2016.ConceptCouplingHalf') -> '_3982.ConceptCouplingHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3982.ConceptCouplingHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_2176.ConceptCouplingHalfLoadCase') -> '_3982.ConceptCouplingHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3982.ConceptCouplingHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_1974.Coupling') -> '_3983.CouplingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3983.CouplingParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_2178.CouplingLoadCase') -> '_3983.CouplingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3983.CouplingParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_1993.CouplingHalf') -> '_3984.CouplingHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3984.CouplingHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_2180.CouplingHalfLoadCase') -> '_3984.CouplingHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3984.CouplingHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_1987.CVT') -> '_3985.CVTParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3985.CVTParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_2182.CVTLoadCase') -> '_3985.CVTParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3985.CVTParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2023.CVTPulley') -> '_3986.CVTPulleyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTPulleyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3986.CVTPulleyParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_2184.CVTPulleyLoadCase') -> '_3986.CVTPulleyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTPulleyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3986.CVTPulleyParametricStudyTool)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2017.Pulley') -> '_3987.PulleyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PulleyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3987.PulleyParametricStudyTool)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_2186.PulleyLoadCase') -> '_3987.PulleyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PulleyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3987.PulleyParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_1967.ShaftHubConnection') -> '_3988.ShaftHubConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftHubConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3988.ShaftHubConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_2188.ShaftHubConnectionLoadCase') -> '_3988.ShaftHubConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftHubConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3988.ShaftHubConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2018.RollingRing') -> '_3989.RollingRingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3989.RollingRingParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_2190.RollingRingLoadCase') -> '_3989.RollingRingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3989.RollingRingParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_1975.RollingRingAssembly') -> '_3990.RollingRingAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3990.RollingRingAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_2192.RollingRingAssemblyLoadCase') -> '_3990.RollingRingAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3990.RollingRingAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_1990.SpringDamper') -> '_3991.SpringDamperParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3991.SpringDamperParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_2194.SpringDamperLoadCase') -> '_3991.SpringDamperParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3991.SpringDamperParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2019.SpringDamperHalf') -> '_3992.SpringDamperHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3992.SpringDamperHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_2196.SpringDamperHalfLoadCase') -> '_3992.SpringDamperHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3992.SpringDamperHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_1976.Synchroniser') -> '_3993.SynchroniserParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3993.SynchroniserParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_2198.SynchroniserLoadCase') -> '_3993.SynchroniserParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3993.SynchroniserParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2024.SynchroniserHalf') -> '_3994.SynchroniserHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3994.SynchroniserHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_2200.SynchroniserHalfLoadCase') -> '_3994.SynchroniserHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3994.SynchroniserHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2020.SynchroniserPart') -> '_3995.SynchroniserPartParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserPartParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3995.SynchroniserPartParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_2202.SynchroniserPartLoadCase') -> '_3995.SynchroniserPartParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserPartParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3995.SynchroniserPartParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2025.SynchroniserSleeve') -> '_3996.SynchroniserSleeveParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserSleeveParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3996.SynchroniserSleeveParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_2204.SynchroniserSleeveLoadCase') -> '_3996.SynchroniserSleeveParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserSleeveParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3996.SynchroniserSleeveParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_1991.TorqueConverter') -> '_3997.TorqueConverterParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3997.TorqueConverterParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_2206.TorqueConverterLoadCase') -> '_3997.TorqueConverterParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3997.TorqueConverterParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2021.TorqueConverterPump') -> '_3998.TorqueConverterPumpParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterPumpParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3998.TorqueConverterPumpParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_2208.TorqueConverterPumpLoadCase') -> '_3998.TorqueConverterPumpParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterPumpParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3998.TorqueConverterPumpParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2022.TorqueConverterTurbine') -> '_3999.TorqueConverterTurbineParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterTurbineParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3999.TorqueConverterTurbineParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_2210.TorqueConverterTurbineLoadCase') -> '_3999.TorqueConverterTurbineParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterTurbineParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3999.TorqueConverterTurbineParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1765.CVTBeltConnection') -> '_4000.CVTBeltConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTBeltConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4000.CVTBeltConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_2212.CVTBeltConnectionLoadCase') -> '_4000.CVTBeltConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTBeltConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4000.CVTBeltConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1760.BeltConnection') -> '_4001.BeltConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BeltConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4001.BeltConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_2213.BeltConnectionLoadCase') -> '_4001.BeltConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BeltConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4001.BeltConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1761.CoaxialConnection') -> '_4002.CoaxialConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CoaxialConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4002.CoaxialConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_2214.CoaxialConnectionLoadCase') -> '_4002.CoaxialConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CoaxialConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4002.CoaxialConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1764.Connection') -> '_4003.ConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4003.ConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_2216.ConnectionLoadCase') -> '_4003.ConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4003.ConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1773.InterMountableComponentConnection') -> '_4004.InterMountableComponentConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.InterMountableComponentConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4004.InterMountableComponentConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_2218.InterMountableComponentConnectionLoadCase') -> '_4004.InterMountableComponentConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.InterMountableComponentConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4004.InterMountableComponentConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1776.PlanetaryConnection') -> '_4005.PlanetaryConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4005.PlanetaryConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_2220.PlanetaryConnectionLoadCase') -> '_4005.PlanetaryConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4005.PlanetaryConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1780.RollingRingConnection') -> '_4006.RollingRingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4006.RollingRingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_2222.RollingRingConnectionLoadCase') -> '_4006.RollingRingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4006.RollingRingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1784.ShaftToMountableComponentConnection') -> '_4007.ShaftToMountableComponentConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftToMountableComponentConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4007.ShaftToMountableComponentConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_2224.ShaftToMountableComponentConnectionLoadCase') -> '_4007.ShaftToMountableComponentConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftToMountableComponentConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4007.ShaftToMountableComponentConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1822.ClutchConnection') -> '_4008.ClutchConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4008.ClutchConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_2225.ClutchConnectionLoadCase') -> '_4008.ClutchConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4008.ClutchConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1824.ConceptCouplingConnection') -> '_4009.ConceptCouplingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4009.ConceptCouplingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_2226.ConceptCouplingConnectionLoadCase') -> '_4009.ConceptCouplingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4009.ConceptCouplingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1826.CouplingConnection') -> '_4010.CouplingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4010.CouplingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_2228.CouplingConnectionLoadCase') -> '_4010.CouplingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4010.CouplingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1828.SpringDamperConnection') -> '_4011.SpringDamperConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4011.SpringDamperConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_2230.SpringDamperConnectionLoadCase') -> '_4011.SpringDamperConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4011.SpringDamperConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1830.TorqueConverterConnection') -> '_4012.TorqueConverterConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4012.TorqueConverterConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_2232.TorqueConverterConnectionLoadCase') -> '_4012.TorqueConverterConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4012.TorqueConverterConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1790.BevelDifferentialGearMesh') -> '_4013.BevelDifferentialGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4013.BevelDifferentialGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_2233.BevelDifferentialGearMeshLoadCase') -> '_4013.BevelDifferentialGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4013.BevelDifferentialGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1794.ConceptGearMesh') -> '_4014.ConceptGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4014.ConceptGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_2234.ConceptGearMeshLoadCase') -> '_4014.ConceptGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4014.ConceptGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1800.FaceGearMesh') -> '_4015.FaceGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4015.FaceGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_2236.FaceGearMeshLoadCase') -> '_4015.FaceGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4015.FaceGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1814.StraightBevelDiffGearMesh') -> '_4016.StraightBevelDiffGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4016.StraightBevelDiffGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_2238.StraightBevelDiffGearMeshLoadCase') -> '_4016.StraightBevelDiffGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4016.StraightBevelDiffGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1792.BevelGearMesh') -> '_4017.BevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4017.BevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2239.BevelGearMeshLoadCase') -> '_4017.BevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4017.BevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1796.ConicalGearMesh') -> '_4018.ConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4018.ConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_2241.ConicalGearMeshLoadCase') -> '_4018.ConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4018.ConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1788.AGMAGleasonConicalGearMesh') -> '_4019.AGMAGleasonConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4019.AGMAGleasonConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_2242.AGMAGleasonConicalGearMeshLoadCase') -> '_4019.AGMAGleasonConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4019.AGMAGleasonConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1798.CylindricalGearMesh') -> '_4020.CylindricalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4020.CylindricalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_2244.CylindricalGearMeshLoadCase') -> '_4020.CylindricalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4020.CylindricalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1804.HypoidGearMesh') -> '_4021.HypoidGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4021.HypoidGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_2246.HypoidGearMeshLoadCase') -> '_4021.HypoidGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4021.HypoidGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1807.KlingelnbergCycloPalloidConicalGearMesh') -> '_4022.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4022.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_2248.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_4022.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4022.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1808.KlingelnbergCycloPalloidHypoidGearMesh') -> '_4023.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4023.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_2250.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_4023.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4023.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_4024.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4024.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2252.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_4024.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4024.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1812.SpiralBevelGearMesh') -> '_4025.SpiralBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4025.SpiralBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2254.SpiralBevelGearMeshLoadCase') -> '_4025.SpiralBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4025.SpiralBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1816.StraightBevelGearMesh') -> '_4026.StraightBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4026.StraightBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2256.StraightBevelGearMeshLoadCase') -> '_4026.StraightBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4026.StraightBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1818.WormGearMesh') -> '_4027.WormGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4027.WormGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_2258.WormGearMeshLoadCase') -> '_4027.WormGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4027.WormGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1820.ZerolBevelGearMesh') -> '_4028.ZerolBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4028.ZerolBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2260.ZerolBevelGearMeshLoadCase') -> '_4028.ZerolBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4028.ZerolBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1802.GearMesh') -> '_4029.GearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4029.GearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_2262.GearMeshLoadCase') -> '_4029.GearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4029.GearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1905.AbstractAssembly') -> '_4030.AbstractAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4030.AbstractAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_2263.AbstractAssemblyLoadCase') -> '_4030.AbstractAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4030.AbstractAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1906.AbstractShaftOrHousing') -> '_4031.AbstractShaftOrHousingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftOrHousingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4031.AbstractShaftOrHousingParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_2264.AbstractShaftOrHousingLoadCase') -> '_4031.AbstractShaftOrHousingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftOrHousingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4031.AbstractShaftOrHousingParametricStudyTool)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1908.Bearing') -> '_4032.BearingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BearingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4032.BearingParametricStudyTool)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_2265.BearingLoadCase') -> '_4032.BearingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BearingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4032.BearingParametricStudyTool)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1910.Bolt') -> '_4033.BoltParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BoltParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4033.BoltParametricStudyTool)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_2266.BoltLoadCase') -> '_4033.BoltParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BoltParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4033.BoltParametricStudyTool)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1911.BoltedJoint') -> '_4034.BoltedJointParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BoltedJointParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4034.BoltedJointParametricStudyTool)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_2267.BoltedJointLoadCase') -> '_4034.BoltedJointParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BoltedJointParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4034.BoltedJointParametricStudyTool)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1912.Component') -> '_4035.ComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4035.ComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_2268.ComponentLoadCase') -> '_4035.ComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4035.ComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1915.Connector') -> '_4036.ConnectorParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectorParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4036.ConnectorParametricStudyTool)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_2270.ConnectorLoadCase') -> '_4036.ConnectorParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectorParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4036.ConnectorParametricStudyTool)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1916.Datum') -> '_4037.DatumParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.DatumParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4037.DatumParametricStudyTool)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_2272.DatumLoadCase') -> '_4037.DatumParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.DatumParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4037.DatumParametricStudyTool)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1919.ExternalCADModel') -> '_4038.ExternalCADModelParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ExternalCADModelParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4038.ExternalCADModelParametricStudyTool)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_2274.ExternalCADModelLoadCase') -> '_4038.ExternalCADModelParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ExternalCADModelParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4038.ExternalCADModelParametricStudyTool)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1920.FlexiblePinAssembly') -> '_4039.FlexiblePinAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FlexiblePinAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4039.FlexiblePinAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_2276.FlexiblePinAssemblyLoadCase') -> '_4039.FlexiblePinAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FlexiblePinAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4039.FlexiblePinAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1904.Assembly') -> '_4040.AssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4040.AssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_2277.AssemblyLoadCase') -> '_4040.AssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4040.AssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1921.GuideDxfModel') -> '_4041.GuideDxfModelParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GuideDxfModelParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4041.GuideDxfModelParametricStudyTool)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_2279.GuideDxfModelLoadCase') -> '_4041.GuideDxfModelParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GuideDxfModelParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4041.GuideDxfModelParametricStudyTool)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1924.ImportedFEComponent') -> '_4042.ImportedFEComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ImportedFEComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4042.ImportedFEComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_2281.ImportedFEComponentLoadCase') -> '_4042.ImportedFEComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ImportedFEComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4042.ImportedFEComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_1926.MassDisc') -> '_4043.MassDiscParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MassDiscParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4043.MassDiscParametricStudyTool)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_2283.MassDiscLoadCase') -> '_4043.MassDiscParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MassDiscParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4043.MassDiscParametricStudyTool)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_1927.MeasurementComponent') -> '_4044.MeasurementComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MeasurementComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4044.MeasurementComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_2285.MeasurementComponentLoadCase') -> '_4044.MeasurementComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MeasurementComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4044.MeasurementComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_1928.MountableComponent') -> '_4045.MountableComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MountableComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4045.MountableComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_2287.MountableComponentLoadCase') -> '_4045.MountableComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MountableComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4045.MountableComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_1929.OilSeal') -> '_4046.OilSealParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.OilSealParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4046.OilSealParametricStudyTool)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_2289.OilSealLoadCase') -> '_4046.OilSealParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.OilSealParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4046.OilSealParametricStudyTool)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_1931.Part') -> '_4047.PartParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PartParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4047.PartParametricStudyTool)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_2291.PartLoadCase') -> '_4047.PartParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PartParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4047.PartParametricStudyTool)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_1932.PlanetCarrier') -> '_4048.PlanetCarrierParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetCarrierParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4048.PlanetCarrierParametricStudyTool)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_2293.PlanetCarrierLoadCase') -> '_4048.PlanetCarrierParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetCarrierParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4048.PlanetCarrierParametricStudyTool)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_1933.PointLoad') -> '_4049.PointLoadParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PointLoadParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4049.PointLoadParametricStudyTool)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_2295.PointLoadLoadCase') -> '_4049.PointLoadParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PointLoadParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4049.PointLoadParametricStudyTool)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_1934.PowerLoad') -> '_4050.PowerLoadParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PowerLoadParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4050.PowerLoadParametricStudyTool)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_2297.PowerLoadLoadCase') -> '_4050.PowerLoadParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PowerLoadParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4050.PowerLoadParametricStudyTool)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_1935.RootAssembly') -> '_4051.RootAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RootAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4051.RootAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_2299.RootAssemblyLoadCase') -> '_4051.RootAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RootAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4051.RootAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_1937.SpecialisedAssembly') -> '_4052.SpecialisedAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpecialisedAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4052.SpecialisedAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_2301.SpecialisedAssemblyLoadCase') -> '_4052.SpecialisedAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpecialisedAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4052.SpecialisedAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_1938.UnbalancedMass') -> '_4053.UnbalancedMassParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.UnbalancedMassParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4053.UnbalancedMassParametricStudyTool)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_2303.UnbalancedMassLoadCase') -> '_4053.UnbalancedMassParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.UnbalancedMassParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4053.UnbalancedMassParametricStudyTool)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_1939.VirtualComponent') -> '_4054.VirtualComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4054.VirtualComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_2305.VirtualComponentLoadCase') -> '_4054.VirtualComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4054.VirtualComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_1942.Shaft') -> '_4055.ShaftParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4055.ShaftParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_2306.ShaftLoadCase') -> '_4055.ShaftParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4055.ShaftParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_1994.ConceptGear') -> '_4056.ConceptGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4056.ConceptGearParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_2307.ConceptGearLoadCase') -> '_4056.ConceptGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4056.ConceptGearParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_1977.ConceptGearSet') -> '_4057.ConceptGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4057.ConceptGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_2308.ConceptGearSetLoadCase') -> '_4057.ConceptGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4057.ConceptGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_1997.FaceGear') -> '_4058.FaceGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4058.FaceGearParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_2310.FaceGearLoadCase') -> '_4058.FaceGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4058.FaceGearParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_1978.FaceGearSet') -> '_4059.FaceGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4059.FaceGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_2312.FaceGearSetLoadCase') -> '_4059.FaceGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4059.FaceGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_1999.AGMAGleasonConicalGear') -> '_4060.AGMAGleasonConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4060.AGMAGleasonConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_2313.AGMAGleasonConicalGearLoadCase') -> '_4060.AGMAGleasonConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4060.AGMAGleasonConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_1979.AGMAGleasonConicalGearSet') -> '_4061.AGMAGleasonConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4061.AGMAGleasonConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_2314.AGMAGleasonConicalGearSetLoadCase') -> '_4061.AGMAGleasonConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4061.AGMAGleasonConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2003.BevelDifferentialGear') -> '_4062.BevelDifferentialGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4062.BevelDifferentialGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_2315.BevelDifferentialGearLoadCase') -> '_4062.BevelDifferentialGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4062.BevelDifferentialGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_1981.BevelDifferentialGearSet') -> '_4063.BevelDifferentialGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4063.BevelDifferentialGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_2316.BevelDifferentialGearSetLoadCase') -> '_4063.BevelDifferentialGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4063.BevelDifferentialGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2008.BevelDifferentialPlanetGear') -> '_4064.BevelDifferentialPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4064.BevelDifferentialPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_2317.BevelDifferentialPlanetGearLoadCase') -> '_4064.BevelDifferentialPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4064.BevelDifferentialPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2009.BevelDifferentialSunGear') -> '_4065.BevelDifferentialSunGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialSunGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4065.BevelDifferentialSunGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_2318.BevelDifferentialSunGearLoadCase') -> '_4065.BevelDifferentialSunGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialSunGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4065.BevelDifferentialSunGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2001.BevelGear') -> '_4066.BevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4066.BevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_2319.BevelGearLoadCase') -> '_4066.BevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4066.BevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_1980.BevelGearSet') -> '_4067.BevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4067.BevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_2320.BevelGearSetLoadCase') -> '_4067.BevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4067.BevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_1995.ConicalGear') -> '_4068.ConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4068.ConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_2322.ConicalGearLoadCase') -> '_4068.ConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4068.ConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_1969.ConicalGearSet') -> '_4069.ConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4069.ConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_2324.ConicalGearSetLoadCase') -> '_4069.ConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4069.ConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_1996.CylindricalGear') -> '_4070.CylindricalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4070.CylindricalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_2326.CylindricalGearLoadCase') -> '_4070.CylindricalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4070.CylindricalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_1968.CylindricalGearSet') -> '_4071.CylindricalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4071.CylindricalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_2328.CylindricalGearSetLoadCase') -> '_4071.CylindricalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4071.CylindricalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2014.CylindricalPlanetGear') -> '_4072.CylindricalPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4072.CylindricalPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_2330.CylindricalPlanetGearLoadCase') -> '_4072.CylindricalPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4072.CylindricalPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_1992.Gear') -> '_4073.GearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4073.GearParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_2332.GearLoadCase') -> '_4073.GearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4073.GearParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_1972.GearSet') -> '_4074.GearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4074.GearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_2334.GearSetLoadCase') -> '_4074.GearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4074.GearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2002.HypoidGear') -> '_4075.HypoidGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4075.HypoidGearParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_2336.HypoidGearLoadCase') -> '_4075.HypoidGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4075.HypoidGearParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_1965.HypoidGearSet') -> '_4076.HypoidGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4076.HypoidGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_2338.HypoidGearSetLoadCase') -> '_4076.HypoidGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4076.HypoidGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2000.KlingelnbergCycloPalloidConicalGear') -> '_4077.KlingelnbergCycloPalloidConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4077.KlingelnbergCycloPalloidConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_2340.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_4077.KlingelnbergCycloPalloidConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4077.KlingelnbergCycloPalloidConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_1971.KlingelnbergCycloPalloidConicalGearSet') -> '_4078.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4078.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_2342.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_4078.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4078.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2012.KlingelnbergCycloPalloidHypoidGear') -> '_4079.KlingelnbergCycloPalloidHypoidGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4079.KlingelnbergCycloPalloidHypoidGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_2344.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_4079.KlingelnbergCycloPalloidHypoidGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4079.KlingelnbergCycloPalloidHypoidGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_1984.KlingelnbergCycloPalloidHypoidGearSet') -> '_4080.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4080.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_2346.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_4080.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4080.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2013.KlingelnbergCycloPalloidSpiralBevelGear') -> '_4081.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4081.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_2348.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_4081.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4081.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_4082.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4082.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_2350.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_4082.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4082.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_1986.PlanetaryGearSet') -> '_4083.PlanetaryGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4083.PlanetaryGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_2351.PlanetaryGearSetLoadCase') -> '_4083.PlanetaryGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4083.PlanetaryGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2004.SpiralBevelGear') -> '_4084.SpiralBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4084.SpiralBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_2353.SpiralBevelGearLoadCase') -> '_4084.SpiralBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4084.SpiralBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_1966.SpiralBevelGearSet') -> '_4085.SpiralBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4085.SpiralBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_2355.SpiralBevelGearSetLoadCase') -> '_4085.SpiralBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4085.SpiralBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2005.StraightBevelDiffGear') -> '_4086.StraightBevelDiffGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4086.StraightBevelDiffGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_2357.StraightBevelDiffGearLoadCase') -> '_4086.StraightBevelDiffGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4086.StraightBevelDiffGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_1982.StraightBevelDiffGearSet') -> '_4087.StraightBevelDiffGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4087.StraightBevelDiffGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_2359.StraightBevelDiffGearSetLoadCase') -> '_4087.StraightBevelDiffGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4087.StraightBevelDiffGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2006.StraightBevelGear') -> '_4088.StraightBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4088.StraightBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_2361.StraightBevelGearLoadCase') -> '_4088.StraightBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4088.StraightBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_1964.StraightBevelGearSet') -> '_4089.StraightBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4089.StraightBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_2363.StraightBevelGearSetLoadCase') -> '_4089.StraightBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4089.StraightBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2010.StraightBevelPlanetGear') -> '_4090.StraightBevelPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4090.StraightBevelPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_2365.StraightBevelPlanetGearLoadCase') -> '_4090.StraightBevelPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4090.StraightBevelPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2011.StraightBevelSunGear') -> '_4091.StraightBevelSunGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelSunGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4091.StraightBevelSunGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_2367.StraightBevelSunGearLoadCase') -> '_4091.StraightBevelSunGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelSunGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4091.StraightBevelSunGearParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_1998.WormGear') -> '_4092.WormGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_4092.WormGearParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_2369.WormGearLoadCase') -> '_4092.WormGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_4092.WormGearParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_1970.WormGearSet') -> '_3975.WormGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3975.WormGearSetParametricStudyTool)(method_result) if method_result else None
