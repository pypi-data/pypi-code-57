'''_2084.py

CompoundParametricStudyToolAnalysis
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
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
    _3500, _3501, _3502, _3503,
    _3504, _3505, _3506, _3507,
    _3508, _3509, _3510, _3511,
    _3512, _3513, _3514, _3515,
    _3516, _3517, _3518, _3519,
    _3520, _3521, _3522, _3523,
    _3524, _3525, _3526, _3527,
    _3528, _3529, _3530, _3531,
    _3532, _3533, _3534, _3535,
    _3536, _3537, _3538, _3539,
    _3540, _3541, _3542, _3543,
    _3544, _3545, _3546, _3547,
    _3548, _3549, _3550, _3551,
    _3552, _3553, _3554, _3555,
    _3556, _3557, _3558, _3559,
    _3560, _3561, _3562, _3563,
    _3564, _3565, _3566, _3567,
    _3568, _3569, _3570, _3571,
    _3572, _3573, _3574, _3575,
    _3576, _3577, _3578, _3579,
    _3580, _3581, _3582, _3583,
    _3584, _3585, _3586, _3587,
    _3588, _3589, _3590, _3591,
    _3592, _3593, _3594, _3595,
    _3596, _3597, _3598, _3599,
    _3600, _3601, _3602, _3603,
    _3604, _3605, _3606, _3607,
    _3608, _3609, _3610, _3611,
    _3612, _3613, _3614, _3615,
    _3616, _3617
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

_COMPOUND_PARAMETRIC_STUDY_TOOL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundParametricStudyToolAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundParametricStudyToolAnalysis',)


class CompoundParametricStudyToolAnalysis(_2081.SingleAnalysis):
    '''CompoundParametricStudyToolAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_PARAMETRIC_STUDY_TOOL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundParametricStudyToolAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_2166.WormGearSetLoadCase') -> '_3500.WormGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3500.WormGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2007.ZerolBevelGear') -> '_3501.ZerolBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3501.ZerolBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_2169.ZerolBevelGearLoadCase') -> '_3501.ZerolBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3501.ZerolBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_1983.ZerolBevelGearSet') -> '_3502.ZerolBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3502.ZerolBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_2171.ZerolBevelGearSetLoadCase') -> '_3502.ZerolBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3502.ZerolBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_1973.BeltDrive') -> '_3503.BeltDriveCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BeltDriveCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3503.BeltDriveCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_2172.BeltDriveLoadCase') -> '_3503.BeltDriveCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BeltDriveCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3503.BeltDriveCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_1988.Clutch') -> '_3504.ClutchCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3504.ClutchCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_2173.ClutchLoadCase') -> '_3504.ClutchCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3504.ClutchCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2015.ClutchHalf') -> '_3505.ClutchHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3505.ClutchHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_2174.ClutchHalfLoadCase') -> '_3505.ClutchHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3505.ClutchHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_1989.ConceptCoupling') -> '_3506.ConceptCouplingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3506.ConceptCouplingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_2175.ConceptCouplingLoadCase') -> '_3506.ConceptCouplingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3506.ConceptCouplingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2016.ConceptCouplingHalf') -> '_3507.ConceptCouplingHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3507.ConceptCouplingHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_2176.ConceptCouplingHalfLoadCase') -> '_3507.ConceptCouplingHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3507.ConceptCouplingHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_1974.Coupling') -> '_3508.CouplingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3508.CouplingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_2178.CouplingLoadCase') -> '_3508.CouplingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3508.CouplingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_1993.CouplingHalf') -> '_3509.CouplingHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3509.CouplingHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_2180.CouplingHalfLoadCase') -> '_3509.CouplingHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3509.CouplingHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_1987.CVT') -> '_3510.CVTCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3510.CVTCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_2182.CVTLoadCase') -> '_3510.CVTCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3510.CVTCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2023.CVTPulley') -> '_3511.CVTPulleyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTPulleyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3511.CVTPulleyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_2184.CVTPulleyLoadCase') -> '_3511.CVTPulleyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTPulleyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3511.CVTPulleyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2017.Pulley') -> '_3512.PulleyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PulleyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3512.PulleyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_2186.PulleyLoadCase') -> '_3512.PulleyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PulleyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3512.PulleyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_1967.ShaftHubConnection') -> '_3513.ShaftHubConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftHubConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3513.ShaftHubConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_2188.ShaftHubConnectionLoadCase') -> '_3513.ShaftHubConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftHubConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3513.ShaftHubConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2018.RollingRing') -> '_3514.RollingRingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3514.RollingRingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_2190.RollingRingLoadCase') -> '_3514.RollingRingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3514.RollingRingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_1975.RollingRingAssembly') -> '_3515.RollingRingAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3515.RollingRingAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_2192.RollingRingAssemblyLoadCase') -> '_3515.RollingRingAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3515.RollingRingAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_1990.SpringDamper') -> '_3516.SpringDamperCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3516.SpringDamperCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_2194.SpringDamperLoadCase') -> '_3516.SpringDamperCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3516.SpringDamperCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2019.SpringDamperHalf') -> '_3517.SpringDamperHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3517.SpringDamperHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_2196.SpringDamperHalfLoadCase') -> '_3517.SpringDamperHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3517.SpringDamperHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_1976.Synchroniser') -> '_3518.SynchroniserCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3518.SynchroniserCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_2198.SynchroniserLoadCase') -> '_3518.SynchroniserCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3518.SynchroniserCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2024.SynchroniserHalf') -> '_3519.SynchroniserHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3519.SynchroniserHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_2200.SynchroniserHalfLoadCase') -> '_3519.SynchroniserHalfCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserHalfCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3519.SynchroniserHalfCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2020.SynchroniserPart') -> '_3520.SynchroniserPartCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserPartCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3520.SynchroniserPartCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_2202.SynchroniserPartLoadCase') -> '_3520.SynchroniserPartCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserPartCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3520.SynchroniserPartCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2025.SynchroniserSleeve') -> '_3521.SynchroniserSleeveCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserSleeveCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3521.SynchroniserSleeveCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_2204.SynchroniserSleeveLoadCase') -> '_3521.SynchroniserSleeveCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SynchroniserSleeveCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3521.SynchroniserSleeveCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_1991.TorqueConverter') -> '_3522.TorqueConverterCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3522.TorqueConverterCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_2206.TorqueConverterLoadCase') -> '_3522.TorqueConverterCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3522.TorqueConverterCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2021.TorqueConverterPump') -> '_3523.TorqueConverterPumpCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterPumpCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3523.TorqueConverterPumpCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_2208.TorqueConverterPumpLoadCase') -> '_3523.TorqueConverterPumpCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterPumpCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3523.TorqueConverterPumpCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2022.TorqueConverterTurbine') -> '_3524.TorqueConverterTurbineCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterTurbineCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3524.TorqueConverterTurbineCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_2210.TorqueConverterTurbineLoadCase') -> '_3524.TorqueConverterTurbineCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterTurbineCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3524.TorqueConverterTurbineCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1765.CVTBeltConnection') -> '_3525.CVTBeltConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTBeltConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3525.CVTBeltConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_2212.CVTBeltConnectionLoadCase') -> '_3525.CVTBeltConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CVTBeltConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3525.CVTBeltConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1760.BeltConnection') -> '_3526.BeltConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BeltConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3526.BeltConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_2213.BeltConnectionLoadCase') -> '_3526.BeltConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BeltConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3526.BeltConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1761.CoaxialConnection') -> '_3527.CoaxialConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CoaxialConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3527.CoaxialConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_2214.CoaxialConnectionLoadCase') -> '_3527.CoaxialConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CoaxialConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3527.CoaxialConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1764.Connection') -> '_3528.ConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3528.ConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_2216.ConnectionLoadCase') -> '_3528.ConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3528.ConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1773.InterMountableComponentConnection') -> '_3529.InterMountableComponentConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.InterMountableComponentConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3529.InterMountableComponentConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_2218.InterMountableComponentConnectionLoadCase') -> '_3529.InterMountableComponentConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.InterMountableComponentConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3529.InterMountableComponentConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1776.PlanetaryConnection') -> '_3530.PlanetaryConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetaryConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3530.PlanetaryConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_2220.PlanetaryConnectionLoadCase') -> '_3530.PlanetaryConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetaryConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3530.PlanetaryConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1780.RollingRingConnection') -> '_3531.RollingRingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3531.RollingRingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_2222.RollingRingConnectionLoadCase') -> '_3531.RollingRingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RollingRingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3531.RollingRingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1784.ShaftToMountableComponentConnection') -> '_3532.ShaftToMountableComponentConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftToMountableComponentConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3532.ShaftToMountableComponentConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_2224.ShaftToMountableComponentConnectionLoadCase') -> '_3532.ShaftToMountableComponentConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftToMountableComponentConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3532.ShaftToMountableComponentConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1822.ClutchConnection') -> '_3533.ClutchConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3533.ClutchConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_2225.ClutchConnectionLoadCase') -> '_3533.ClutchConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ClutchConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3533.ClutchConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1824.ConceptCouplingConnection') -> '_3534.ConceptCouplingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3534.ConceptCouplingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_2226.ConceptCouplingConnectionLoadCase') -> '_3534.ConceptCouplingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptCouplingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3534.ConceptCouplingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1826.CouplingConnection') -> '_3535.CouplingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3535.CouplingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_2228.CouplingConnectionLoadCase') -> '_3535.CouplingConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CouplingConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3535.CouplingConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1828.SpringDamperConnection') -> '_3536.SpringDamperConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3536.SpringDamperConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_2230.SpringDamperConnectionLoadCase') -> '_3536.SpringDamperConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpringDamperConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3536.SpringDamperConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1830.TorqueConverterConnection') -> '_3537.TorqueConverterConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3537.TorqueConverterConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_2232.TorqueConverterConnectionLoadCase') -> '_3537.TorqueConverterConnectionCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.TorqueConverterConnectionCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3537.TorqueConverterConnectionCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1790.BevelDifferentialGearMesh') -> '_3538.BevelDifferentialGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3538.BevelDifferentialGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_2233.BevelDifferentialGearMeshLoadCase') -> '_3538.BevelDifferentialGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3538.BevelDifferentialGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1794.ConceptGearMesh') -> '_3539.ConceptGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3539.ConceptGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_2234.ConceptGearMeshLoadCase') -> '_3539.ConceptGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3539.ConceptGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1800.FaceGearMesh') -> '_3540.FaceGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3540.FaceGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_2236.FaceGearMeshLoadCase') -> '_3540.FaceGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3540.FaceGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1814.StraightBevelDiffGearMesh') -> '_3541.StraightBevelDiffGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3541.StraightBevelDiffGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_2238.StraightBevelDiffGearMeshLoadCase') -> '_3541.StraightBevelDiffGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3541.StraightBevelDiffGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1792.BevelGearMesh') -> '_3542.BevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3542.BevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2239.BevelGearMeshLoadCase') -> '_3542.BevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3542.BevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1796.ConicalGearMesh') -> '_3543.ConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3543.ConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_2241.ConicalGearMeshLoadCase') -> '_3543.ConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3543.ConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1788.AGMAGleasonConicalGearMesh') -> '_3544.AGMAGleasonConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3544.AGMAGleasonConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_2242.AGMAGleasonConicalGearMeshLoadCase') -> '_3544.AGMAGleasonConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3544.AGMAGleasonConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1798.CylindricalGearMesh') -> '_3545.CylindricalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3545.CylindricalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_2244.CylindricalGearMeshLoadCase') -> '_3545.CylindricalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3545.CylindricalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1804.HypoidGearMesh') -> '_3546.HypoidGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3546.HypoidGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_2246.HypoidGearMeshLoadCase') -> '_3546.HypoidGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3546.HypoidGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1807.KlingelnbergCycloPalloidConicalGearMesh') -> '_3547.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3547.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_2248.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_3547.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3547.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1808.KlingelnbergCycloPalloidHypoidGearMesh') -> '_3548.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3548.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_2250.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_3548.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3548.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_3549.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3549.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2252.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_3549.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3549.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1812.SpiralBevelGearMesh') -> '_3550.SpiralBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3550.SpiralBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2254.SpiralBevelGearMeshLoadCase') -> '_3550.SpiralBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3550.SpiralBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1816.StraightBevelGearMesh') -> '_3551.StraightBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3551.StraightBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2256.StraightBevelGearMeshLoadCase') -> '_3551.StraightBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3551.StraightBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1818.WormGearMesh') -> '_3552.WormGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3552.WormGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_2258.WormGearMeshLoadCase') -> '_3552.WormGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3552.WormGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1820.ZerolBevelGearMesh') -> '_3553.ZerolBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3553.ZerolBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2260.ZerolBevelGearMeshLoadCase') -> '_3553.ZerolBevelGearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ZerolBevelGearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3553.ZerolBevelGearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1802.GearMesh') -> '_3554.GearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3554.GearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_2262.GearMeshLoadCase') -> '_3554.GearMeshCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearMeshCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3554.GearMeshCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1905.AbstractAssembly') -> '_3555.AbstractAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AbstractAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3555.AbstractAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_2263.AbstractAssemblyLoadCase') -> '_3555.AbstractAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AbstractAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3555.AbstractAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1906.AbstractShaftOrHousing') -> '_3556.AbstractShaftOrHousingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AbstractShaftOrHousingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3556.AbstractShaftOrHousingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_2264.AbstractShaftOrHousingLoadCase') -> '_3556.AbstractShaftOrHousingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AbstractShaftOrHousingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3556.AbstractShaftOrHousingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1908.Bearing') -> '_3557.BearingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BearingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3557.BearingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_2265.BearingLoadCase') -> '_3557.BearingCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BearingCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3557.BearingCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1910.Bolt') -> '_3558.BoltCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BoltCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3558.BoltCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_2266.BoltLoadCase') -> '_3558.BoltCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BoltCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3558.BoltCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1911.BoltedJoint') -> '_3559.BoltedJointCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BoltedJointCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3559.BoltedJointCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_2267.BoltedJointLoadCase') -> '_3559.BoltedJointCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BoltedJointCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3559.BoltedJointCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1912.Component') -> '_3560.ComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3560.ComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_2268.ComponentLoadCase') -> '_3560.ComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3560.ComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1915.Connector') -> '_3561.ConnectorCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConnectorCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3561.ConnectorCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_2270.ConnectorLoadCase') -> '_3561.ConnectorCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConnectorCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3561.ConnectorCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1916.Datum') -> '_3562.DatumCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.DatumCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3562.DatumCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_2272.DatumLoadCase') -> '_3562.DatumCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.DatumCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3562.DatumCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1919.ExternalCADModel') -> '_3563.ExternalCADModelCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ExternalCADModelCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3563.ExternalCADModelCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_2274.ExternalCADModelLoadCase') -> '_3563.ExternalCADModelCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ExternalCADModelCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3563.ExternalCADModelCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1920.FlexiblePinAssembly') -> '_3564.FlexiblePinAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FlexiblePinAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3564.FlexiblePinAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_2276.FlexiblePinAssemblyLoadCase') -> '_3564.FlexiblePinAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FlexiblePinAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3564.FlexiblePinAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1904.Assembly') -> '_3565.AssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3565.AssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_2277.AssemblyLoadCase') -> '_3565.AssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3565.AssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1921.GuideDxfModel') -> '_3566.GuideDxfModelCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GuideDxfModelCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3566.GuideDxfModelCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_2279.GuideDxfModelLoadCase') -> '_3566.GuideDxfModelCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GuideDxfModelCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3566.GuideDxfModelCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1924.ImportedFEComponent') -> '_3567.ImportedFEComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ImportedFEComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3567.ImportedFEComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_2281.ImportedFEComponentLoadCase') -> '_3567.ImportedFEComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ImportedFEComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3567.ImportedFEComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_1926.MassDisc') -> '_3568.MassDiscCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MassDiscCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3568.MassDiscCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_2283.MassDiscLoadCase') -> '_3568.MassDiscCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MassDiscCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3568.MassDiscCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_1927.MeasurementComponent') -> '_3569.MeasurementComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MeasurementComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3569.MeasurementComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_2285.MeasurementComponentLoadCase') -> '_3569.MeasurementComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MeasurementComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3569.MeasurementComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_1928.MountableComponent') -> '_3570.MountableComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MountableComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3570.MountableComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_2287.MountableComponentLoadCase') -> '_3570.MountableComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.MountableComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3570.MountableComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_1929.OilSeal') -> '_3571.OilSealCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.OilSealCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3571.OilSealCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_2289.OilSealLoadCase') -> '_3571.OilSealCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.OilSealCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3571.OilSealCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_1931.Part') -> '_3572.PartCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PartCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3572.PartCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_2291.PartLoadCase') -> '_3572.PartCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PartCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3572.PartCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_1932.PlanetCarrier') -> '_3573.PlanetCarrierCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetCarrierCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3573.PlanetCarrierCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_2293.PlanetCarrierLoadCase') -> '_3573.PlanetCarrierCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetCarrierCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3573.PlanetCarrierCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_1933.PointLoad') -> '_3574.PointLoadCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PointLoadCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3574.PointLoadCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_2295.PointLoadLoadCase') -> '_3574.PointLoadCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PointLoadCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3574.PointLoadCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_1934.PowerLoad') -> '_3575.PowerLoadCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PowerLoadCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3575.PowerLoadCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_2297.PowerLoadLoadCase') -> '_3575.PowerLoadCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PowerLoadCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3575.PowerLoadCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_1935.RootAssembly') -> '_3576.RootAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RootAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3576.RootAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_2299.RootAssemblyLoadCase') -> '_3576.RootAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.RootAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3576.RootAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_1937.SpecialisedAssembly') -> '_3577.SpecialisedAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpecialisedAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3577.SpecialisedAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_2301.SpecialisedAssemblyLoadCase') -> '_3577.SpecialisedAssemblyCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpecialisedAssemblyCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3577.SpecialisedAssemblyCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_1938.UnbalancedMass') -> '_3578.UnbalancedMassCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.UnbalancedMassCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3578.UnbalancedMassCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_2303.UnbalancedMassLoadCase') -> '_3578.UnbalancedMassCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.UnbalancedMassCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3578.UnbalancedMassCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_1939.VirtualComponent') -> '_3579.VirtualComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.VirtualComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3579.VirtualComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_2305.VirtualComponentLoadCase') -> '_3579.VirtualComponentCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.VirtualComponentCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3579.VirtualComponentCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_1942.Shaft') -> '_3580.ShaftCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3580.ShaftCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_2306.ShaftLoadCase') -> '_3580.ShaftCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ShaftCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3580.ShaftCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_1994.ConceptGear') -> '_3581.ConceptGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3581.ConceptGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_2307.ConceptGearLoadCase') -> '_3581.ConceptGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3581.ConceptGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_1977.ConceptGearSet') -> '_3582.ConceptGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3582.ConceptGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_2308.ConceptGearSetLoadCase') -> '_3582.ConceptGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConceptGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3582.ConceptGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_1997.FaceGear') -> '_3583.FaceGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3583.FaceGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_2310.FaceGearLoadCase') -> '_3583.FaceGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3583.FaceGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_1978.FaceGearSet') -> '_3584.FaceGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3584.FaceGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_2312.FaceGearSetLoadCase') -> '_3584.FaceGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.FaceGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3584.FaceGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_1999.AGMAGleasonConicalGear') -> '_3585.AGMAGleasonConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3585.AGMAGleasonConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_2313.AGMAGleasonConicalGearLoadCase') -> '_3585.AGMAGleasonConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3585.AGMAGleasonConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_1979.AGMAGleasonConicalGearSet') -> '_3586.AGMAGleasonConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3586.AGMAGleasonConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_2314.AGMAGleasonConicalGearSetLoadCase') -> '_3586.AGMAGleasonConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.AGMAGleasonConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3586.AGMAGleasonConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2003.BevelDifferentialGear') -> '_3587.BevelDifferentialGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3587.BevelDifferentialGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_2315.BevelDifferentialGearLoadCase') -> '_3587.BevelDifferentialGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3587.BevelDifferentialGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_1981.BevelDifferentialGearSet') -> '_3588.BevelDifferentialGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3588.BevelDifferentialGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_2316.BevelDifferentialGearSetLoadCase') -> '_3588.BevelDifferentialGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3588.BevelDifferentialGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2008.BevelDifferentialPlanetGear') -> '_3589.BevelDifferentialPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3589.BevelDifferentialPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_2317.BevelDifferentialPlanetGearLoadCase') -> '_3589.BevelDifferentialPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3589.BevelDifferentialPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2009.BevelDifferentialSunGear') -> '_3590.BevelDifferentialSunGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialSunGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3590.BevelDifferentialSunGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_2318.BevelDifferentialSunGearLoadCase') -> '_3590.BevelDifferentialSunGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelDifferentialSunGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3590.BevelDifferentialSunGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2001.BevelGear') -> '_3591.BevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3591.BevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_2319.BevelGearLoadCase') -> '_3591.BevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3591.BevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_1980.BevelGearSet') -> '_3592.BevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3592.BevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_2320.BevelGearSetLoadCase') -> '_3592.BevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3592.BevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_1995.ConicalGear') -> '_3593.ConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3593.ConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_2322.ConicalGearLoadCase') -> '_3593.ConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3593.ConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_1969.ConicalGearSet') -> '_3594.ConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3594.ConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_2324.ConicalGearSetLoadCase') -> '_3594.ConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.ConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3594.ConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_1996.CylindricalGear') -> '_3595.CylindricalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3595.CylindricalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_2326.CylindricalGearLoadCase') -> '_3595.CylindricalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3595.CylindricalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_1968.CylindricalGearSet') -> '_3596.CylindricalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3596.CylindricalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_2328.CylindricalGearSetLoadCase') -> '_3596.CylindricalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3596.CylindricalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2014.CylindricalPlanetGear') -> '_3597.CylindricalPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3597.CylindricalPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_2330.CylindricalPlanetGearLoadCase') -> '_3597.CylindricalPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.CylindricalPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3597.CylindricalPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_1992.Gear') -> '_3598.GearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3598.GearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_2332.GearLoadCase') -> '_3598.GearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3598.GearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_1972.GearSet') -> '_3599.GearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3599.GearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_2334.GearSetLoadCase') -> '_3599.GearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.GearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3599.GearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2002.HypoidGear') -> '_3600.HypoidGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3600.HypoidGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_2336.HypoidGearLoadCase') -> '_3600.HypoidGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3600.HypoidGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_1965.HypoidGearSet') -> '_3601.HypoidGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3601.HypoidGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_2338.HypoidGearSetLoadCase') -> '_3601.HypoidGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.HypoidGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3601.HypoidGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2000.KlingelnbergCycloPalloidConicalGear') -> '_3602.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3602.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_2340.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_3602.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3602.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_1971.KlingelnbergCycloPalloidConicalGearSet') -> '_3603.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3603.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_2342.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_3603.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3603.KlingelnbergCycloPalloidConicalGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2012.KlingelnbergCycloPalloidHypoidGear') -> '_3604.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3604.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_2344.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_3604.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3604.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_1984.KlingelnbergCycloPalloidHypoidGearSet') -> '_3605.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3605.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_2346.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_3605.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3605.KlingelnbergCycloPalloidHypoidGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2013.KlingelnbergCycloPalloidSpiralBevelGear') -> '_3606.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3606.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_2348.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_3606.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3606.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_3607.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3607.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_2350.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_3607.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3607.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_1986.PlanetaryGearSet') -> '_3608.PlanetaryGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetaryGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3608.PlanetaryGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_2351.PlanetaryGearSetLoadCase') -> '_3608.PlanetaryGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.PlanetaryGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3608.PlanetaryGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2004.SpiralBevelGear') -> '_3609.SpiralBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3609.SpiralBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_2353.SpiralBevelGearLoadCase') -> '_3609.SpiralBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3609.SpiralBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_1966.SpiralBevelGearSet') -> '_3610.SpiralBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3610.SpiralBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_2355.SpiralBevelGearSetLoadCase') -> '_3610.SpiralBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.SpiralBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3610.SpiralBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2005.StraightBevelDiffGear') -> '_3611.StraightBevelDiffGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3611.StraightBevelDiffGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_2357.StraightBevelDiffGearLoadCase') -> '_3611.StraightBevelDiffGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3611.StraightBevelDiffGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_1982.StraightBevelDiffGearSet') -> '_3612.StraightBevelDiffGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3612.StraightBevelDiffGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_2359.StraightBevelDiffGearSetLoadCase') -> '_3612.StraightBevelDiffGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelDiffGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3612.StraightBevelDiffGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2006.StraightBevelGear') -> '_3613.StraightBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3613.StraightBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_2361.StraightBevelGearLoadCase') -> '_3613.StraightBevelGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3613.StraightBevelGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_1964.StraightBevelGearSet') -> '_3614.StraightBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3614.StraightBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_2363.StraightBevelGearSetLoadCase') -> '_3614.StraightBevelGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3614.StraightBevelGearSetCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2010.StraightBevelPlanetGear') -> '_3615.StraightBevelPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3615.StraightBevelPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_2365.StraightBevelPlanetGearLoadCase') -> '_3615.StraightBevelPlanetGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelPlanetGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3615.StraightBevelPlanetGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2011.StraightBevelSunGear') -> '_3616.StraightBevelSunGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelSunGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3616.StraightBevelSunGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_2367.StraightBevelSunGearLoadCase') -> '_3616.StraightBevelSunGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.StraightBevelSunGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3616.StraightBevelSunGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_1998.WormGear') -> '_3617.WormGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3617.WormGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_2369.WormGearLoadCase') -> '_3617.WormGearCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3617.WormGearCompoundParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_1970.WormGearSet') -> '_3500.WormGearSetCompoundParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.compound.WormGearSetCompoundParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3500.WormGearSetCompoundParametricStudyTool)(method_result) if method_result else None
