'''_2082.py

AdvancedSystemDeflectionAnalysis
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
from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
    _3382, _3383, _3384, _3385,
    _3386, _3387, _3388, _3389,
    _3390, _3391, _3392, _3393,
    _3394, _3395, _3396, _3397,
    _3398, _3399, _3400, _3401,
    _3402, _3403, _3404, _3405,
    _3406, _3407, _3408, _3409,
    _3410, _3411, _3412, _3413,
    _3414, _3415, _3416, _3417,
    _3418, _3419, _3420, _3421,
    _3422, _3423, _3424, _3425,
    _3426, _3427, _3428, _3429,
    _3430, _3431, _3432, _3433,
    _3434, _3435, _3436, _3437,
    _3438, _3439, _3440, _3441,
    _3442, _3443, _3444, _3445,
    _3446, _3447, _3448, _3449,
    _3450, _3451, _3452, _3453,
    _3454, _3455, _3456, _3457,
    _3458, _3459, _3460, _3461,
    _3462, _3463, _3464, _3465,
    _3466, _3467, _3468, _3469,
    _3470, _3471, _3472, _3473,
    _3474, _3475, _3476, _3477,
    _3478, _3479, _3480, _3481,
    _3482, _3483, _3484, _3485,
    _3486, _3487, _3488, _3489,
    _3490, _3491, _3492, _3493,
    _3494, _3495, _3496, _3497,
    _3498, _3499
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

_ADVANCED_SYSTEM_DEFLECTION_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'AdvancedSystemDeflectionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AdvancedSystemDeflectionAnalysis',)


class AdvancedSystemDeflectionAnalysis(_2081.SingleAnalysis):
    '''AdvancedSystemDeflectionAnalysis

    This is a mastapy class.
    '''

    TYPE = _ADVANCED_SYSTEM_DEFLECTION_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'AdvancedSystemDeflectionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_2166.WormGearSetLoadCase') -> '_3382.WormGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3382.WormGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2007.ZerolBevelGear') -> '_3383.ZerolBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3383.ZerolBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_2169.ZerolBevelGearLoadCase') -> '_3383.ZerolBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3383.ZerolBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_1983.ZerolBevelGearSet') -> '_3384.ZerolBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3384.ZerolBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_2171.ZerolBevelGearSetLoadCase') -> '_3384.ZerolBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3384.ZerolBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_1973.BeltDrive') -> '_3385.BeltDriveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltDriveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3385.BeltDriveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_2172.BeltDriveLoadCase') -> '_3385.BeltDriveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltDriveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3385.BeltDriveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_1988.Clutch') -> '_3386.ClutchAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3386.ClutchAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_2173.ClutchLoadCase') -> '_3386.ClutchAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3386.ClutchAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2015.ClutchHalf') -> '_3387.ClutchHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3387.ClutchHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_2174.ClutchHalfLoadCase') -> '_3387.ClutchHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3387.ClutchHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_1989.ConceptCoupling') -> '_3388.ConceptCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3388.ConceptCouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_2175.ConceptCouplingLoadCase') -> '_3388.ConceptCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3388.ConceptCouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2016.ConceptCouplingHalf') -> '_3389.ConceptCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3389.ConceptCouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_2176.ConceptCouplingHalfLoadCase') -> '_3389.ConceptCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3389.ConceptCouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_1974.Coupling') -> '_3390.CouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3390.CouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_2178.CouplingLoadCase') -> '_3390.CouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3390.CouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_1993.CouplingHalf') -> '_3391.CouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3391.CouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_2180.CouplingHalfLoadCase') -> '_3391.CouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3391.CouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_1987.CVT') -> '_3392.CVTAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3392.CVTAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_2182.CVTLoadCase') -> '_3392.CVTAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3392.CVTAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2023.CVTPulley') -> '_3393.CVTPulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTPulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3393.CVTPulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_2184.CVTPulleyLoadCase') -> '_3393.CVTPulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTPulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3393.CVTPulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2017.Pulley') -> '_3394.PulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3394.PulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_2186.PulleyLoadCase') -> '_3394.PulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3394.PulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_1967.ShaftHubConnection') -> '_3395.ShaftHubConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftHubConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3395.ShaftHubConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_2188.ShaftHubConnectionLoadCase') -> '_3395.ShaftHubConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftHubConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3395.ShaftHubConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2018.RollingRing') -> '_3396.RollingRingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3396.RollingRingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_2190.RollingRingLoadCase') -> '_3396.RollingRingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3396.RollingRingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_1975.RollingRingAssembly') -> '_3397.RollingRingAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3397.RollingRingAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_2192.RollingRingAssemblyLoadCase') -> '_3397.RollingRingAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3397.RollingRingAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_1990.SpringDamper') -> '_3398.SpringDamperAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3398.SpringDamperAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_2194.SpringDamperLoadCase') -> '_3398.SpringDamperAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3398.SpringDamperAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2019.SpringDamperHalf') -> '_3399.SpringDamperHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3399.SpringDamperHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_2196.SpringDamperHalfLoadCase') -> '_3399.SpringDamperHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3399.SpringDamperHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_1976.Synchroniser') -> '_3400.SynchroniserAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3400.SynchroniserAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_2198.SynchroniserLoadCase') -> '_3400.SynchroniserAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3400.SynchroniserAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2024.SynchroniserHalf') -> '_3401.SynchroniserHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3401.SynchroniserHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_2200.SynchroniserHalfLoadCase') -> '_3401.SynchroniserHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3401.SynchroniserHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2020.SynchroniserPart') -> '_3402.SynchroniserPartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserPartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3402.SynchroniserPartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_2202.SynchroniserPartLoadCase') -> '_3402.SynchroniserPartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserPartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3402.SynchroniserPartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2025.SynchroniserSleeve') -> '_3403.SynchroniserSleeveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserSleeveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3403.SynchroniserSleeveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_2204.SynchroniserSleeveLoadCase') -> '_3403.SynchroniserSleeveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserSleeveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3403.SynchroniserSleeveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_1991.TorqueConverter') -> '_3404.TorqueConverterAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3404.TorqueConverterAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_2206.TorqueConverterLoadCase') -> '_3404.TorqueConverterAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3404.TorqueConverterAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2021.TorqueConverterPump') -> '_3405.TorqueConverterPumpAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterPumpAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3405.TorqueConverterPumpAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_2208.TorqueConverterPumpLoadCase') -> '_3405.TorqueConverterPumpAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterPumpAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3405.TorqueConverterPumpAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2022.TorqueConverterTurbine') -> '_3406.TorqueConverterTurbineAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterTurbineAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3406.TorqueConverterTurbineAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_2210.TorqueConverterTurbineLoadCase') -> '_3406.TorqueConverterTurbineAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterTurbineAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3406.TorqueConverterTurbineAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1765.CVTBeltConnection') -> '_3407.CVTBeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTBeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3407.CVTBeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_2212.CVTBeltConnectionLoadCase') -> '_3407.CVTBeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTBeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3407.CVTBeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1760.BeltConnection') -> '_3408.BeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3408.BeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_2213.BeltConnectionLoadCase') -> '_3408.BeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3408.BeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1761.CoaxialConnection') -> '_3409.CoaxialConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CoaxialConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3409.CoaxialConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_2214.CoaxialConnectionLoadCase') -> '_3409.CoaxialConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CoaxialConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3409.CoaxialConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1764.Connection') -> '_3410.ConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3410.ConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_2216.ConnectionLoadCase') -> '_3410.ConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3410.ConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1773.InterMountableComponentConnection') -> '_3411.InterMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.InterMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3411.InterMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_2218.InterMountableComponentConnectionLoadCase') -> '_3411.InterMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.InterMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3411.InterMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1776.PlanetaryConnection') -> '_3412.PlanetaryConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3412.PlanetaryConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_2220.PlanetaryConnectionLoadCase') -> '_3412.PlanetaryConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3412.PlanetaryConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1780.RollingRingConnection') -> '_3413.RollingRingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3413.RollingRingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_2222.RollingRingConnectionLoadCase') -> '_3413.RollingRingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3413.RollingRingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1784.ShaftToMountableComponentConnection') -> '_3414.ShaftToMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3414.ShaftToMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_2224.ShaftToMountableComponentConnectionLoadCase') -> '_3414.ShaftToMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3414.ShaftToMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1822.ClutchConnection') -> '_3415.ClutchConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3415.ClutchConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_2225.ClutchConnectionLoadCase') -> '_3415.ClutchConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3415.ClutchConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1824.ConceptCouplingConnection') -> '_3416.ConceptCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3416.ConceptCouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_2226.ConceptCouplingConnectionLoadCase') -> '_3416.ConceptCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3416.ConceptCouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1826.CouplingConnection') -> '_3417.CouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3417.CouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_2228.CouplingConnectionLoadCase') -> '_3417.CouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3417.CouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1828.SpringDamperConnection') -> '_3418.SpringDamperConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3418.SpringDamperConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_2230.SpringDamperConnectionLoadCase') -> '_3418.SpringDamperConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3418.SpringDamperConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1830.TorqueConverterConnection') -> '_3419.TorqueConverterConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3419.TorqueConverterConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_2232.TorqueConverterConnectionLoadCase') -> '_3419.TorqueConverterConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3419.TorqueConverterConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1790.BevelDifferentialGearMesh') -> '_3420.BevelDifferentialGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3420.BevelDifferentialGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_2233.BevelDifferentialGearMeshLoadCase') -> '_3420.BevelDifferentialGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3420.BevelDifferentialGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1794.ConceptGearMesh') -> '_3421.ConceptGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3421.ConceptGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_2234.ConceptGearMeshLoadCase') -> '_3421.ConceptGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3421.ConceptGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1800.FaceGearMesh') -> '_3422.FaceGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3422.FaceGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_2236.FaceGearMeshLoadCase') -> '_3422.FaceGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3422.FaceGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1814.StraightBevelDiffGearMesh') -> '_3423.StraightBevelDiffGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3423.StraightBevelDiffGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_2238.StraightBevelDiffGearMeshLoadCase') -> '_3423.StraightBevelDiffGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3423.StraightBevelDiffGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1792.BevelGearMesh') -> '_3424.BevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3424.BevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2239.BevelGearMeshLoadCase') -> '_3424.BevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3424.BevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1796.ConicalGearMesh') -> '_3425.ConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3425.ConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_2241.ConicalGearMeshLoadCase') -> '_3425.ConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3425.ConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1788.AGMAGleasonConicalGearMesh') -> '_3426.AGMAGleasonConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3426.AGMAGleasonConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_2242.AGMAGleasonConicalGearMeshLoadCase') -> '_3426.AGMAGleasonConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3426.AGMAGleasonConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1798.CylindricalGearMesh') -> '_3427.CylindricalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3427.CylindricalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_2244.CylindricalGearMeshLoadCase') -> '_3427.CylindricalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3427.CylindricalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1804.HypoidGearMesh') -> '_3428.HypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3428.HypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_2246.HypoidGearMeshLoadCase') -> '_3428.HypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3428.HypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1807.KlingelnbergCycloPalloidConicalGearMesh') -> '_3429.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3429.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_2248.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_3429.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3429.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1808.KlingelnbergCycloPalloidHypoidGearMesh') -> '_3430.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3430.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_2250.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_3430.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3430.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_3431.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3431.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2252.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_3431.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3431.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1812.SpiralBevelGearMesh') -> '_3432.SpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3432.SpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2254.SpiralBevelGearMeshLoadCase') -> '_3432.SpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3432.SpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1816.StraightBevelGearMesh') -> '_3433.StraightBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3433.StraightBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2256.StraightBevelGearMeshLoadCase') -> '_3433.StraightBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3433.StraightBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1818.WormGearMesh') -> '_3434.WormGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3434.WormGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_2258.WormGearMeshLoadCase') -> '_3434.WormGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3434.WormGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1820.ZerolBevelGearMesh') -> '_3435.ZerolBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3435.ZerolBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2260.ZerolBevelGearMeshLoadCase') -> '_3435.ZerolBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3435.ZerolBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1802.GearMesh') -> '_3436.GearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3436.GearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_2262.GearMeshLoadCase') -> '_3436.GearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3436.GearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1905.AbstractAssembly') -> '_3437.AbstractAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3437.AbstractAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_2263.AbstractAssemblyLoadCase') -> '_3437.AbstractAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3437.AbstractAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1906.AbstractShaftOrHousing') -> '_3438.AbstractShaftOrHousingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftOrHousingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3438.AbstractShaftOrHousingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_2264.AbstractShaftOrHousingLoadCase') -> '_3438.AbstractShaftOrHousingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftOrHousingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3438.AbstractShaftOrHousingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1908.Bearing') -> '_3439.BearingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BearingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3439.BearingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_2265.BearingLoadCase') -> '_3439.BearingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BearingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3439.BearingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1910.Bolt') -> '_3440.BoltAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3440.BoltAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_2266.BoltLoadCase') -> '_3440.BoltAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3440.BoltAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1911.BoltedJoint') -> '_3441.BoltedJointAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltedJointAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3441.BoltedJointAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_2267.BoltedJointLoadCase') -> '_3441.BoltedJointAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltedJointAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3441.BoltedJointAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1912.Component') -> '_3442.ComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3442.ComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_2268.ComponentLoadCase') -> '_3442.ComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3442.ComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1915.Connector') -> '_3443.ConnectorAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectorAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3443.ConnectorAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_2270.ConnectorLoadCase') -> '_3443.ConnectorAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectorAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3443.ConnectorAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1916.Datum') -> '_3444.DatumAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.DatumAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3444.DatumAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_2272.DatumLoadCase') -> '_3444.DatumAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.DatumAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3444.DatumAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1919.ExternalCADModel') -> '_3445.ExternalCADModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ExternalCADModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3445.ExternalCADModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_2274.ExternalCADModelLoadCase') -> '_3445.ExternalCADModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ExternalCADModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3445.ExternalCADModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1920.FlexiblePinAssembly') -> '_3446.FlexiblePinAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FlexiblePinAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3446.FlexiblePinAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_2276.FlexiblePinAssemblyLoadCase') -> '_3446.FlexiblePinAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FlexiblePinAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3446.FlexiblePinAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1904.Assembly') -> '_3447.AssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3447.AssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_2277.AssemblyLoadCase') -> '_3447.AssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3447.AssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1921.GuideDxfModel') -> '_3448.GuideDxfModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GuideDxfModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3448.GuideDxfModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_2279.GuideDxfModelLoadCase') -> '_3448.GuideDxfModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GuideDxfModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3448.GuideDxfModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1924.ImportedFEComponent') -> '_3449.ImportedFEComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ImportedFEComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3449.ImportedFEComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_2281.ImportedFEComponentLoadCase') -> '_3449.ImportedFEComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ImportedFEComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3449.ImportedFEComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_1926.MassDisc') -> '_3450.MassDiscAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MassDiscAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3450.MassDiscAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_2283.MassDiscLoadCase') -> '_3450.MassDiscAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MassDiscAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3450.MassDiscAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_1927.MeasurementComponent') -> '_3451.MeasurementComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MeasurementComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3451.MeasurementComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_2285.MeasurementComponentLoadCase') -> '_3451.MeasurementComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MeasurementComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3451.MeasurementComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_1928.MountableComponent') -> '_3452.MountableComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MountableComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3452.MountableComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_2287.MountableComponentLoadCase') -> '_3452.MountableComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MountableComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3452.MountableComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_1929.OilSeal') -> '_3453.OilSealAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.OilSealAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3453.OilSealAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_2289.OilSealLoadCase') -> '_3453.OilSealAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.OilSealAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3453.OilSealAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_1931.Part') -> '_3454.PartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3454.PartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_2291.PartLoadCase') -> '_3454.PartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3454.PartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_1932.PlanetCarrier') -> '_3455.PlanetCarrierAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetCarrierAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3455.PlanetCarrierAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_2293.PlanetCarrierLoadCase') -> '_3455.PlanetCarrierAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetCarrierAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3455.PlanetCarrierAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_1933.PointLoad') -> '_3456.PointLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PointLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3456.PointLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_2295.PointLoadLoadCase') -> '_3456.PointLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PointLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3456.PointLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_1934.PowerLoad') -> '_3457.PowerLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PowerLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3457.PowerLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_2297.PowerLoadLoadCase') -> '_3457.PowerLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PowerLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3457.PowerLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_1935.RootAssembly') -> '_3458.RootAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RootAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3458.RootAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_2299.RootAssemblyLoadCase') -> '_3458.RootAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RootAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3458.RootAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_1937.SpecialisedAssembly') -> '_3459.SpecialisedAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpecialisedAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3459.SpecialisedAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_2301.SpecialisedAssemblyLoadCase') -> '_3459.SpecialisedAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpecialisedAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3459.SpecialisedAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_1938.UnbalancedMass') -> '_3460.UnbalancedMassAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.UnbalancedMassAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3460.UnbalancedMassAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_2303.UnbalancedMassLoadCase') -> '_3460.UnbalancedMassAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.UnbalancedMassAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3460.UnbalancedMassAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_1939.VirtualComponent') -> '_3461.VirtualComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.VirtualComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3461.VirtualComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_2305.VirtualComponentLoadCase') -> '_3461.VirtualComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.VirtualComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3461.VirtualComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_1942.Shaft') -> '_3462.ShaftAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3462.ShaftAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_2306.ShaftLoadCase') -> '_3462.ShaftAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3462.ShaftAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_1994.ConceptGear') -> '_3463.ConceptGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3463.ConceptGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_2307.ConceptGearLoadCase') -> '_3463.ConceptGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3463.ConceptGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_1977.ConceptGearSet') -> '_3464.ConceptGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3464.ConceptGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_2308.ConceptGearSetLoadCase') -> '_3464.ConceptGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3464.ConceptGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_1997.FaceGear') -> '_3465.FaceGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3465.FaceGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_2310.FaceGearLoadCase') -> '_3465.FaceGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3465.FaceGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_1978.FaceGearSet') -> '_3466.FaceGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3466.FaceGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_2312.FaceGearSetLoadCase') -> '_3466.FaceGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3466.FaceGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_1999.AGMAGleasonConicalGear') -> '_3467.AGMAGleasonConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3467.AGMAGleasonConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_2313.AGMAGleasonConicalGearLoadCase') -> '_3467.AGMAGleasonConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3467.AGMAGleasonConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_1979.AGMAGleasonConicalGearSet') -> '_3468.AGMAGleasonConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3468.AGMAGleasonConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_2314.AGMAGleasonConicalGearSetLoadCase') -> '_3468.AGMAGleasonConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3468.AGMAGleasonConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2003.BevelDifferentialGear') -> '_3469.BevelDifferentialGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3469.BevelDifferentialGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_2315.BevelDifferentialGearLoadCase') -> '_3469.BevelDifferentialGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3469.BevelDifferentialGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_1981.BevelDifferentialGearSet') -> '_3470.BevelDifferentialGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3470.BevelDifferentialGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_2316.BevelDifferentialGearSetLoadCase') -> '_3470.BevelDifferentialGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3470.BevelDifferentialGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2008.BevelDifferentialPlanetGear') -> '_3471.BevelDifferentialPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3471.BevelDifferentialPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_2317.BevelDifferentialPlanetGearLoadCase') -> '_3471.BevelDifferentialPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3471.BevelDifferentialPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2009.BevelDifferentialSunGear') -> '_3472.BevelDifferentialSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3472.BevelDifferentialSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_2318.BevelDifferentialSunGearLoadCase') -> '_3472.BevelDifferentialSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3472.BevelDifferentialSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2001.BevelGear') -> '_3473.BevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3473.BevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_2319.BevelGearLoadCase') -> '_3473.BevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3473.BevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_1980.BevelGearSet') -> '_3474.BevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3474.BevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_2320.BevelGearSetLoadCase') -> '_3474.BevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3474.BevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_1995.ConicalGear') -> '_3475.ConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3475.ConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_2322.ConicalGearLoadCase') -> '_3475.ConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3475.ConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_1969.ConicalGearSet') -> '_3476.ConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3476.ConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_2324.ConicalGearSetLoadCase') -> '_3476.ConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3476.ConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_1996.CylindricalGear') -> '_3477.CylindricalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3477.CylindricalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_2326.CylindricalGearLoadCase') -> '_3477.CylindricalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3477.CylindricalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_1968.CylindricalGearSet') -> '_3478.CylindricalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3478.CylindricalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_2328.CylindricalGearSetLoadCase') -> '_3478.CylindricalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3478.CylindricalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2014.CylindricalPlanetGear') -> '_3479.CylindricalPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3479.CylindricalPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_2330.CylindricalPlanetGearLoadCase') -> '_3479.CylindricalPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3479.CylindricalPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_1992.Gear') -> '_3480.GearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3480.GearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_2332.GearLoadCase') -> '_3480.GearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3480.GearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_1972.GearSet') -> '_3481.GearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3481.GearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_2334.GearSetLoadCase') -> '_3481.GearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3481.GearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2002.HypoidGear') -> '_3482.HypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3482.HypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_2336.HypoidGearLoadCase') -> '_3482.HypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3482.HypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_1965.HypoidGearSet') -> '_3483.HypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3483.HypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_2338.HypoidGearSetLoadCase') -> '_3483.HypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3483.HypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2000.KlingelnbergCycloPalloidConicalGear') -> '_3484.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3484.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_2340.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_3484.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3484.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_1971.KlingelnbergCycloPalloidConicalGearSet') -> '_3485.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3485.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_2342.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_3485.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3485.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2012.KlingelnbergCycloPalloidHypoidGear') -> '_3486.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3486.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_2344.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_3486.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3486.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_1984.KlingelnbergCycloPalloidHypoidGearSet') -> '_3487.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3487.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_2346.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_3487.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3487.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2013.KlingelnbergCycloPalloidSpiralBevelGear') -> '_3488.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3488.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_2348.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_3488.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3488.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_3489.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3489.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_2350.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_3489.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3489.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_1986.PlanetaryGearSet') -> '_3490.PlanetaryGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3490.PlanetaryGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_2351.PlanetaryGearSetLoadCase') -> '_3490.PlanetaryGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3490.PlanetaryGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2004.SpiralBevelGear') -> '_3491.SpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3491.SpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_2353.SpiralBevelGearLoadCase') -> '_3491.SpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3491.SpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_1966.SpiralBevelGearSet') -> '_3492.SpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3492.SpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_2355.SpiralBevelGearSetLoadCase') -> '_3492.SpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3492.SpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2005.StraightBevelDiffGear') -> '_3493.StraightBevelDiffGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3493.StraightBevelDiffGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_2357.StraightBevelDiffGearLoadCase') -> '_3493.StraightBevelDiffGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3493.StraightBevelDiffGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_1982.StraightBevelDiffGearSet') -> '_3494.StraightBevelDiffGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3494.StraightBevelDiffGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_2359.StraightBevelDiffGearSetLoadCase') -> '_3494.StraightBevelDiffGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3494.StraightBevelDiffGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2006.StraightBevelGear') -> '_3495.StraightBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3495.StraightBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_2361.StraightBevelGearLoadCase') -> '_3495.StraightBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3495.StraightBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_1964.StraightBevelGearSet') -> '_3496.StraightBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3496.StraightBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_2363.StraightBevelGearSetLoadCase') -> '_3496.StraightBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3496.StraightBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2010.StraightBevelPlanetGear') -> '_3497.StraightBevelPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3497.StraightBevelPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_2365.StraightBevelPlanetGearLoadCase') -> '_3497.StraightBevelPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3497.StraightBevelPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2011.StraightBevelSunGear') -> '_3498.StraightBevelSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3498.StraightBevelSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_2367.StraightBevelSunGearLoadCase') -> '_3498.StraightBevelSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3498.StraightBevelSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_1998.WormGear') -> '_3499.WormGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3499.WormGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_2369.WormGearLoadCase') -> '_3499.WormGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3499.WormGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_1970.WormGearSet') -> '_3382.WormGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3382.WormGearSetAdvancedSystemDeflection)(method_result) if method_result else None
