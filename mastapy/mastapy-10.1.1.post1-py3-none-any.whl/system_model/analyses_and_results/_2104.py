'''_2104.py

SystemDeflectionAnalysis
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
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2167, _2168, _2170, _2143,
    _2156, _2155, _2162, _2161,
    _2177, _2179, _2181, _2183,
    _2185, _2187, _2189, _2191,
    _2193, _2195, _2197, _2199,
    _2201, _2203, _2205, _2207,
    _2209, _2211, _2142, _2157,
    _2215, _2217, _2219, _2221,
    _2223, _2154, _2160, _2227,
    _2229, _2231, _2144, _2163,
    _2235, _2237, _2149, _2240,
    _2137, _2243, _2245, _2247,
    _2249, _2251, _2253, _2255,
    _2257, _2259, _2261, _2135,
    _2136, _2141, _2153, _2152,
    _2158, _2269, _2271, _2273,
    _2275, _2140, _2278, _2280,
    _2282, _2284, _2286, _2288,
    _2290, _2292, _2294, _2296,
    _2298, _2300, _2302, _2304,
    _2066, _2165, _2164, _2309,
    _2311, _2139, _2138, _2146,
    _2145, _2147, _2148, _2151,
    _2150, _2321, _2323, _2325,
    _2327, _2329, _2331, _2333,
    _2335, _2337, _2339, _2341,
    _2343, _2345, _2347, _2349,
    _2352, _2354, _2356, _2358,
    _2360, _2362, _2364, _2366,
    _2368
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

_SYSTEM_DEFLECTION_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'SystemDeflectionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemDeflectionAnalysis',)


class SystemDeflectionAnalysis(_2081.SingleAnalysis):
    '''SystemDeflectionAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYSTEM_DEFLECTION_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SystemDeflectionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_2166.WormGearSetLoadCase') -> '_2167.WormGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.WormGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2167.WormGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2007.ZerolBevelGear') -> '_2168.ZerolBevelGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ZerolBevelGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2168.ZerolBevelGearSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_2169.ZerolBevelGearLoadCase') -> '_2168.ZerolBevelGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ZerolBevelGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2168.ZerolBevelGearSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_1983.ZerolBevelGearSet') -> '_2170.ZerolBevelGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ZerolBevelGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2170.ZerolBevelGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_2171.ZerolBevelGearSetLoadCase') -> '_2170.ZerolBevelGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ZerolBevelGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2170.ZerolBevelGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_1973.BeltDrive') -> '_2143.BeltDriveSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BeltDriveSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2143.BeltDriveSystemDeflection)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_2172.BeltDriveLoadCase') -> '_2143.BeltDriveSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BeltDriveSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2143.BeltDriveSystemDeflection)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_1988.Clutch') -> '_2156.ClutchSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ClutchSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2156.ClutchSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_2173.ClutchLoadCase') -> '_2156.ClutchSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ClutchSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2156.ClutchSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2015.ClutchHalf') -> '_2155.ClutchHalfSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ClutchHalfSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2155.ClutchHalfSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_2174.ClutchHalfLoadCase') -> '_2155.ClutchHalfSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ClutchHalfSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2155.ClutchHalfSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_1989.ConceptCoupling') -> '_2162.ConceptCouplingSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptCouplingSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2162.ConceptCouplingSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_2175.ConceptCouplingLoadCase') -> '_2162.ConceptCouplingSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptCouplingSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2162.ConceptCouplingSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2016.ConceptCouplingHalf') -> '_2161.ConceptCouplingHalfSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptCouplingHalfSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2161.ConceptCouplingHalfSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_2176.ConceptCouplingHalfLoadCase') -> '_2161.ConceptCouplingHalfSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptCouplingHalfSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2161.ConceptCouplingHalfSystemDeflection)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_1974.Coupling') -> '_2177.CouplingSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CouplingSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2177.CouplingSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_2178.CouplingLoadCase') -> '_2177.CouplingSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CouplingSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2177.CouplingSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_1993.CouplingHalf') -> '_2179.CouplingHalfSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CouplingHalfSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2179.CouplingHalfSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_2180.CouplingHalfLoadCase') -> '_2179.CouplingHalfSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CouplingHalfSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2179.CouplingHalfSystemDeflection)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_1987.CVT') -> '_2181.CVTSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CVTSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2181.CVTSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_2182.CVTLoadCase') -> '_2181.CVTSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CVTSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2181.CVTSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2023.CVTPulley') -> '_2183.CVTPulleySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CVTPulleySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2183.CVTPulleySystemDeflection)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_2184.CVTPulleyLoadCase') -> '_2183.CVTPulleySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CVTPulleySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2183.CVTPulleySystemDeflection)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2017.Pulley') -> '_2185.PulleySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PulleySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2185.PulleySystemDeflection)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_2186.PulleyLoadCase') -> '_2185.PulleySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PulleySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2185.PulleySystemDeflection)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_1967.ShaftHubConnection') -> '_2187.ShaftHubConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ShaftHubConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2187.ShaftHubConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_2188.ShaftHubConnectionLoadCase') -> '_2187.ShaftHubConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ShaftHubConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2187.ShaftHubConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2018.RollingRing') -> '_2189.RollingRingSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.RollingRingSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2189.RollingRingSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_2190.RollingRingLoadCase') -> '_2189.RollingRingSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.RollingRingSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2189.RollingRingSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_1975.RollingRingAssembly') -> '_2191.RollingRingAssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.RollingRingAssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2191.RollingRingAssemblySystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_2192.RollingRingAssemblyLoadCase') -> '_2191.RollingRingAssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.RollingRingAssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2191.RollingRingAssemblySystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_1990.SpringDamper') -> '_2193.SpringDamperSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpringDamperSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2193.SpringDamperSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_2194.SpringDamperLoadCase') -> '_2193.SpringDamperSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpringDamperSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2193.SpringDamperSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2019.SpringDamperHalf') -> '_2195.SpringDamperHalfSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpringDamperHalfSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2195.SpringDamperHalfSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_2196.SpringDamperHalfLoadCase') -> '_2195.SpringDamperHalfSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpringDamperHalfSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2195.SpringDamperHalfSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_1976.Synchroniser') -> '_2197.SynchroniserSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SynchroniserSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2197.SynchroniserSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_2198.SynchroniserLoadCase') -> '_2197.SynchroniserSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SynchroniserSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2197.SynchroniserSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2024.SynchroniserHalf') -> '_2199.SynchroniserHalfSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SynchroniserHalfSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2199.SynchroniserHalfSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_2200.SynchroniserHalfLoadCase') -> '_2199.SynchroniserHalfSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SynchroniserHalfSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2199.SynchroniserHalfSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2020.SynchroniserPart') -> '_2201.SynchroniserPartSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SynchroniserPartSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2201.SynchroniserPartSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_2202.SynchroniserPartLoadCase') -> '_2201.SynchroniserPartSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SynchroniserPartSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2201.SynchroniserPartSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2025.SynchroniserSleeve') -> '_2203.SynchroniserSleeveSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SynchroniserSleeveSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2203.SynchroniserSleeveSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_2204.SynchroniserSleeveLoadCase') -> '_2203.SynchroniserSleeveSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SynchroniserSleeveSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2203.SynchroniserSleeveSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_1991.TorqueConverter') -> '_2205.TorqueConverterSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2205.TorqueConverterSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_2206.TorqueConverterLoadCase') -> '_2205.TorqueConverterSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2205.TorqueConverterSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2021.TorqueConverterPump') -> '_2207.TorqueConverterPumpSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterPumpSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2207.TorqueConverterPumpSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_2208.TorqueConverterPumpLoadCase') -> '_2207.TorqueConverterPumpSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterPumpSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2207.TorqueConverterPumpSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2022.TorqueConverterTurbine') -> '_2209.TorqueConverterTurbineSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterTurbineSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2209.TorqueConverterTurbineSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_2210.TorqueConverterTurbineLoadCase') -> '_2209.TorqueConverterTurbineSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterTurbineSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2209.TorqueConverterTurbineSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1765.CVTBeltConnection') -> '_2211.CVTBeltConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CVTBeltConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2211.CVTBeltConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_2212.CVTBeltConnectionLoadCase') -> '_2211.CVTBeltConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CVTBeltConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2211.CVTBeltConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1760.BeltConnection') -> '_2142.BeltConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BeltConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2142.BeltConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_2213.BeltConnectionLoadCase') -> '_2142.BeltConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BeltConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2142.BeltConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1761.CoaxialConnection') -> '_2157.CoaxialConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CoaxialConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2157.CoaxialConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_2214.CoaxialConnectionLoadCase') -> '_2157.CoaxialConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CoaxialConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2157.CoaxialConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1764.Connection') -> '_2215.ConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2215.ConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_2216.ConnectionLoadCase') -> '_2215.ConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2215.ConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1773.InterMountableComponentConnection') -> '_2217.InterMountableComponentConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.InterMountableComponentConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2217.InterMountableComponentConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_2218.InterMountableComponentConnectionLoadCase') -> '_2217.InterMountableComponentConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.InterMountableComponentConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2217.InterMountableComponentConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1776.PlanetaryConnection') -> '_2219.PlanetaryConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PlanetaryConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2219.PlanetaryConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_2220.PlanetaryConnectionLoadCase') -> '_2219.PlanetaryConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PlanetaryConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2219.PlanetaryConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1780.RollingRingConnection') -> '_2221.RollingRingConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.RollingRingConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2221.RollingRingConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_2222.RollingRingConnectionLoadCase') -> '_2221.RollingRingConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.RollingRingConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2221.RollingRingConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1784.ShaftToMountableComponentConnection') -> '_2223.ShaftToMountableComponentConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ShaftToMountableComponentConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2223.ShaftToMountableComponentConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_2224.ShaftToMountableComponentConnectionLoadCase') -> '_2223.ShaftToMountableComponentConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ShaftToMountableComponentConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2223.ShaftToMountableComponentConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1822.ClutchConnection') -> '_2154.ClutchConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ClutchConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2154.ClutchConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_2225.ClutchConnectionLoadCase') -> '_2154.ClutchConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ClutchConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2154.ClutchConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1824.ConceptCouplingConnection') -> '_2160.ConceptCouplingConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptCouplingConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2160.ConceptCouplingConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_2226.ConceptCouplingConnectionLoadCase') -> '_2160.ConceptCouplingConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptCouplingConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2160.ConceptCouplingConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1826.CouplingConnection') -> '_2227.CouplingConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CouplingConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2227.CouplingConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_2228.CouplingConnectionLoadCase') -> '_2227.CouplingConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CouplingConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2227.CouplingConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1828.SpringDamperConnection') -> '_2229.SpringDamperConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpringDamperConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2229.SpringDamperConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_2230.SpringDamperConnectionLoadCase') -> '_2229.SpringDamperConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpringDamperConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2229.SpringDamperConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1830.TorqueConverterConnection') -> '_2231.TorqueConverterConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2231.TorqueConverterConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_2232.TorqueConverterConnectionLoadCase') -> '_2231.TorqueConverterConnectionSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterConnectionSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2231.TorqueConverterConnectionSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1790.BevelDifferentialGearMesh') -> '_2144.BevelDifferentialGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2144.BevelDifferentialGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_2233.BevelDifferentialGearMeshLoadCase') -> '_2144.BevelDifferentialGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2144.BevelDifferentialGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1794.ConceptGearMesh') -> '_2163.ConceptGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2163.ConceptGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_2234.ConceptGearMeshLoadCase') -> '_2163.ConceptGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2163.ConceptGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1800.FaceGearMesh') -> '_2235.FaceGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.FaceGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2235.FaceGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_2236.FaceGearMeshLoadCase') -> '_2235.FaceGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.FaceGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2235.FaceGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1814.StraightBevelDiffGearMesh') -> '_2237.StraightBevelDiffGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelDiffGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2237.StraightBevelDiffGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_2238.StraightBevelDiffGearMeshLoadCase') -> '_2237.StraightBevelDiffGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelDiffGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2237.StraightBevelDiffGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1792.BevelGearMesh') -> '_2149.BevelGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2149.BevelGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2239.BevelGearMeshLoadCase') -> '_2149.BevelGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2149.BevelGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1796.ConicalGearMesh') -> '_2240.ConicalGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConicalGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2240.ConicalGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_2241.ConicalGearMeshLoadCase') -> '_2240.ConicalGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConicalGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2240.ConicalGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1788.AGMAGleasonConicalGearMesh') -> '_2137.AGMAGleasonConicalGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AGMAGleasonConicalGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2137.AGMAGleasonConicalGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_2242.AGMAGleasonConicalGearMeshLoadCase') -> '_2137.AGMAGleasonConicalGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AGMAGleasonConicalGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2137.AGMAGleasonConicalGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1798.CylindricalGearMesh') -> '_2243.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearMeshSystemDeflectionWithLTCAResults
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2243.CylindricalGearMeshSystemDeflectionWithLTCAResults)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_2244.CylindricalGearMeshLoadCase') -> '_2243.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearMeshSystemDeflectionWithLTCAResults
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2243.CylindricalGearMeshSystemDeflectionWithLTCAResults)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1804.HypoidGearMesh') -> '_2245.HypoidGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.HypoidGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2245.HypoidGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_2246.HypoidGearMeshLoadCase') -> '_2245.HypoidGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.HypoidGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2245.HypoidGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1807.KlingelnbergCycloPalloidConicalGearMesh') -> '_2247.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2247.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_2248.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_2247.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2247.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1808.KlingelnbergCycloPalloidHypoidGearMesh') -> '_2249.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2249.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_2250.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_2249.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2249.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_2251.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2251.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2252.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_2251.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2251.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1812.SpiralBevelGearMesh') -> '_2253.SpiralBevelGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpiralBevelGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2253.SpiralBevelGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2254.SpiralBevelGearMeshLoadCase') -> '_2253.SpiralBevelGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpiralBevelGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2253.SpiralBevelGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1816.StraightBevelGearMesh') -> '_2255.StraightBevelGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2255.StraightBevelGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2256.StraightBevelGearMeshLoadCase') -> '_2255.StraightBevelGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2255.StraightBevelGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1818.WormGearMesh') -> '_2257.WormGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.WormGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2257.WormGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_2258.WormGearMeshLoadCase') -> '_2257.WormGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.WormGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2257.WormGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1820.ZerolBevelGearMesh') -> '_2259.ZerolBevelGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ZerolBevelGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2259.ZerolBevelGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_2260.ZerolBevelGearMeshLoadCase') -> '_2259.ZerolBevelGearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ZerolBevelGearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2259.ZerolBevelGearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1802.GearMesh') -> '_2261.GearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.GearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2261.GearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_2262.GearMeshLoadCase') -> '_2261.GearMeshSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.GearMeshSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2261.GearMeshSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1905.AbstractAssembly') -> '_2135.AbstractAssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AbstractAssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2135.AbstractAssemblySystemDeflection)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_2263.AbstractAssemblyLoadCase') -> '_2135.AbstractAssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AbstractAssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2135.AbstractAssemblySystemDeflection)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1906.AbstractShaftOrHousing') -> '_2136.AbstractShaftOrHousingSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AbstractShaftOrHousingSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2136.AbstractShaftOrHousingSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_2264.AbstractShaftOrHousingLoadCase') -> '_2136.AbstractShaftOrHousingSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AbstractShaftOrHousingSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2136.AbstractShaftOrHousingSystemDeflection)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1908.Bearing') -> '_2141.BearingSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BearingSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2141.BearingSystemDeflection)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_2265.BearingLoadCase') -> '_2141.BearingSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BearingSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2141.BearingSystemDeflection)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1910.Bolt') -> '_2153.BoltSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BoltSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2153.BoltSystemDeflection)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_2266.BoltLoadCase') -> '_2153.BoltSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BoltSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2153.BoltSystemDeflection)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1911.BoltedJoint') -> '_2152.BoltedJointSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BoltedJointSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2152.BoltedJointSystemDeflection)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_2267.BoltedJointLoadCase') -> '_2152.BoltedJointSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BoltedJointSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2152.BoltedJointSystemDeflection)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1912.Component') -> '_2158.ComponentSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ComponentSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2158.ComponentSystemDeflection)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_2268.ComponentLoadCase') -> '_2158.ComponentSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ComponentSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2158.ComponentSystemDeflection)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1915.Connector') -> '_2269.ConnectorSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConnectorSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2269.ConnectorSystemDeflection)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_2270.ConnectorLoadCase') -> '_2269.ConnectorSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConnectorSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2269.ConnectorSystemDeflection)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1916.Datum') -> '_2271.DatumSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.DatumSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2271.DatumSystemDeflection)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_2272.DatumLoadCase') -> '_2271.DatumSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.DatumSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2271.DatumSystemDeflection)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1919.ExternalCADModel') -> '_2273.ExternalCADModelSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ExternalCADModelSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2273.ExternalCADModelSystemDeflection)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_2274.ExternalCADModelLoadCase') -> '_2273.ExternalCADModelSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ExternalCADModelSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2273.ExternalCADModelSystemDeflection)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1920.FlexiblePinAssembly') -> '_2275.FlexiblePinAssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.FlexiblePinAssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2275.FlexiblePinAssemblySystemDeflection)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_2276.FlexiblePinAssemblyLoadCase') -> '_2275.FlexiblePinAssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.FlexiblePinAssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2275.FlexiblePinAssemblySystemDeflection)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1904.Assembly') -> '_2140.AssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2140.AssemblySystemDeflection)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_2277.AssemblyLoadCase') -> '_2140.AssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2140.AssemblySystemDeflection)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1921.GuideDxfModel') -> '_2278.GuideDxfModelSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.GuideDxfModelSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2278.GuideDxfModelSystemDeflection)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_2279.GuideDxfModelLoadCase') -> '_2278.GuideDxfModelSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.GuideDxfModelSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2278.GuideDxfModelSystemDeflection)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1924.ImportedFEComponent') -> '_2280.ImportedFEComponentSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ImportedFEComponentSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2280.ImportedFEComponentSystemDeflection)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_2281.ImportedFEComponentLoadCase') -> '_2280.ImportedFEComponentSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ImportedFEComponentSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2280.ImportedFEComponentSystemDeflection)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_1926.MassDisc') -> '_2282.MassDiscSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.MassDiscSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2282.MassDiscSystemDeflection)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_2283.MassDiscLoadCase') -> '_2282.MassDiscSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.MassDiscSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2282.MassDiscSystemDeflection)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_1927.MeasurementComponent') -> '_2284.MeasurementComponentSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.MeasurementComponentSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2284.MeasurementComponentSystemDeflection)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_2285.MeasurementComponentLoadCase') -> '_2284.MeasurementComponentSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.MeasurementComponentSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2284.MeasurementComponentSystemDeflection)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_1928.MountableComponent') -> '_2286.MountableComponentSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.MountableComponentSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2286.MountableComponentSystemDeflection)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_2287.MountableComponentLoadCase') -> '_2286.MountableComponentSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.MountableComponentSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2286.MountableComponentSystemDeflection)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_1929.OilSeal') -> '_2288.OilSealSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.OilSealSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2288.OilSealSystemDeflection)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_2289.OilSealLoadCase') -> '_2288.OilSealSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.OilSealSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2288.OilSealSystemDeflection)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_1931.Part') -> '_2290.PartSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PartSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2290.PartSystemDeflection)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_2291.PartLoadCase') -> '_2290.PartSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PartSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2290.PartSystemDeflection)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_1932.PlanetCarrier') -> '_2292.PlanetCarrierSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PlanetCarrierSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2292.PlanetCarrierSystemDeflection)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_2293.PlanetCarrierLoadCase') -> '_2292.PlanetCarrierSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PlanetCarrierSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2292.PlanetCarrierSystemDeflection)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_1933.PointLoad') -> '_2294.PointLoadSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PointLoadSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2294.PointLoadSystemDeflection)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_2295.PointLoadLoadCase') -> '_2294.PointLoadSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PointLoadSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2294.PointLoadSystemDeflection)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_1934.PowerLoad') -> '_2296.PowerLoadSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PowerLoadSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2296.PowerLoadSystemDeflection)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_2297.PowerLoadLoadCase') -> '_2296.PowerLoadSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.PowerLoadSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2296.PowerLoadSystemDeflection)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_1935.RootAssembly') -> '_2298.RootAssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2298.RootAssemblySystemDeflection)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_2299.RootAssemblyLoadCase') -> '_2298.RootAssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2298.RootAssemblySystemDeflection)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_1937.SpecialisedAssembly') -> '_2300.SpecialisedAssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpecialisedAssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2300.SpecialisedAssemblySystemDeflection)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_2301.SpecialisedAssemblyLoadCase') -> '_2300.SpecialisedAssemblySystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpecialisedAssemblySystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2300.SpecialisedAssemblySystemDeflection)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_1938.UnbalancedMass') -> '_2302.UnbalancedMassSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.UnbalancedMassSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2302.UnbalancedMassSystemDeflection)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_2303.UnbalancedMassLoadCase') -> '_2302.UnbalancedMassSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.UnbalancedMassSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2302.UnbalancedMassSystemDeflection)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_1939.VirtualComponent') -> '_2304.VirtualComponentSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.VirtualComponentSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2304.VirtualComponentSystemDeflection)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_2305.VirtualComponentLoadCase') -> '_2304.VirtualComponentSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.VirtualComponentSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2304.VirtualComponentSystemDeflection)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_1942.Shaft') -> '_2066.ShaftSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ShaftSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2066.ShaftSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_2306.ShaftLoadCase') -> '_2066.ShaftSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ShaftSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2066.ShaftSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_1994.ConceptGear') -> '_2165.ConceptGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2165.ConceptGearSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_2307.ConceptGearLoadCase') -> '_2165.ConceptGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2165.ConceptGearSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_1977.ConceptGearSet') -> '_2164.ConceptGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2164.ConceptGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_2308.ConceptGearSetLoadCase') -> '_2164.ConceptGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConceptGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2164.ConceptGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_1997.FaceGear') -> '_2309.FaceGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.FaceGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2309.FaceGearSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_2310.FaceGearLoadCase') -> '_2309.FaceGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.FaceGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2309.FaceGearSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_1978.FaceGearSet') -> '_2311.FaceGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.FaceGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2311.FaceGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_2312.FaceGearSetLoadCase') -> '_2311.FaceGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.FaceGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2311.FaceGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_1999.AGMAGleasonConicalGear') -> '_2139.AGMAGleasonConicalGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AGMAGleasonConicalGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2139.AGMAGleasonConicalGearSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_2313.AGMAGleasonConicalGearLoadCase') -> '_2139.AGMAGleasonConicalGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AGMAGleasonConicalGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2139.AGMAGleasonConicalGearSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_1979.AGMAGleasonConicalGearSet') -> '_2138.AGMAGleasonConicalGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AGMAGleasonConicalGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2138.AGMAGleasonConicalGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_2314.AGMAGleasonConicalGearSetLoadCase') -> '_2138.AGMAGleasonConicalGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.AGMAGleasonConicalGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2138.AGMAGleasonConicalGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2003.BevelDifferentialGear') -> '_2146.BevelDifferentialGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2146.BevelDifferentialGearSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_2315.BevelDifferentialGearLoadCase') -> '_2146.BevelDifferentialGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2146.BevelDifferentialGearSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_1981.BevelDifferentialGearSet') -> '_2145.BevelDifferentialGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2145.BevelDifferentialGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_2316.BevelDifferentialGearSetLoadCase') -> '_2145.BevelDifferentialGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2145.BevelDifferentialGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2008.BevelDifferentialPlanetGear') -> '_2147.BevelDifferentialPlanetGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialPlanetGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2147.BevelDifferentialPlanetGearSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_2317.BevelDifferentialPlanetGearLoadCase') -> '_2147.BevelDifferentialPlanetGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialPlanetGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2147.BevelDifferentialPlanetGearSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2009.BevelDifferentialSunGear') -> '_2148.BevelDifferentialSunGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialSunGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2148.BevelDifferentialSunGearSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_2318.BevelDifferentialSunGearLoadCase') -> '_2148.BevelDifferentialSunGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialSunGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2148.BevelDifferentialSunGearSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2001.BevelGear') -> '_2151.BevelGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2151.BevelGearSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_2319.BevelGearLoadCase') -> '_2151.BevelGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2151.BevelGearSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_1980.BevelGearSet') -> '_2150.BevelGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2150.BevelGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_2320.BevelGearSetLoadCase') -> '_2150.BevelGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.BevelGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2150.BevelGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_1995.ConicalGear') -> '_2321.ConicalGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2321.ConicalGearSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_2322.ConicalGearLoadCase') -> '_2321.ConicalGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2321.ConicalGearSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_1969.ConicalGearSet') -> '_2323.ConicalGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2323.ConicalGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_2324.ConicalGearSetLoadCase') -> '_2323.ConicalGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2323.ConicalGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_1996.CylindricalGear') -> '_2325.CylindricalGearSystemDeflectionWithLTCAResults':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSystemDeflectionWithLTCAResults
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2325.CylindricalGearSystemDeflectionWithLTCAResults)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_2326.CylindricalGearLoadCase') -> '_2325.CylindricalGearSystemDeflectionWithLTCAResults':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSystemDeflectionWithLTCAResults
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2325.CylindricalGearSystemDeflectionWithLTCAResults)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_1968.CylindricalGearSet') -> '_2327.CylindricalGearSetSystemDeflectionWithLTCAResults':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSetSystemDeflectionWithLTCAResults
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2327.CylindricalGearSetSystemDeflectionWithLTCAResults)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_2328.CylindricalGearSetLoadCase') -> '_2327.CylindricalGearSetSystemDeflectionWithLTCAResults':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSetSystemDeflectionWithLTCAResults
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2327.CylindricalGearSetSystemDeflectionWithLTCAResults)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2014.CylindricalPlanetGear') -> '_2329.CylindricalPlanetGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CylindricalPlanetGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2329.CylindricalPlanetGearSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_2330.CylindricalPlanetGearLoadCase') -> '_2329.CylindricalPlanetGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CylindricalPlanetGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2329.CylindricalPlanetGearSystemDeflection)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_1992.Gear') -> '_2331.GearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.GearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2331.GearSystemDeflection)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_2332.GearLoadCase') -> '_2331.GearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.GearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2331.GearSystemDeflection)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_1972.GearSet') -> '_2333.GearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.GearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2333.GearSetSystemDeflection)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_2334.GearSetLoadCase') -> '_2333.GearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.GearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2333.GearSetSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2002.HypoidGear') -> '_2335.HypoidGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.HypoidGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2335.HypoidGearSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_2336.HypoidGearLoadCase') -> '_2335.HypoidGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.HypoidGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2335.HypoidGearSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_1965.HypoidGearSet') -> '_2337.HypoidGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.HypoidGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2337.HypoidGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_2338.HypoidGearSetLoadCase') -> '_2337.HypoidGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.HypoidGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2337.HypoidGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2000.KlingelnbergCycloPalloidConicalGear') -> '_2339.KlingelnbergCycloPalloidConicalGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2339.KlingelnbergCycloPalloidConicalGearSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_2340.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_2339.KlingelnbergCycloPalloidConicalGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2339.KlingelnbergCycloPalloidConicalGearSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_1971.KlingelnbergCycloPalloidConicalGearSet') -> '_2341.KlingelnbergCycloPalloidConicalGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2341.KlingelnbergCycloPalloidConicalGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_2342.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_2341.KlingelnbergCycloPalloidConicalGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2341.KlingelnbergCycloPalloidConicalGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2012.KlingelnbergCycloPalloidHypoidGear') -> '_2343.KlingelnbergCycloPalloidHypoidGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidHypoidGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2343.KlingelnbergCycloPalloidHypoidGearSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_2344.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_2343.KlingelnbergCycloPalloidHypoidGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidHypoidGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2343.KlingelnbergCycloPalloidHypoidGearSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_1984.KlingelnbergCycloPalloidHypoidGearSet') -> '_2345.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2345.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_2346.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_2345.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2345.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2013.KlingelnbergCycloPalloidSpiralBevelGear') -> '_2347.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2347.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_2348.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_2347.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2347.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_2349.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2349.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_2350.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_2349.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2349.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_1986.PlanetaryGearSet') -> '_2327.CylindricalGearSetSystemDeflectionWithLTCAResults':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSetSystemDeflectionWithLTCAResults
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2327.CylindricalGearSetSystemDeflectionWithLTCAResults)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_2351.PlanetaryGearSetLoadCase') -> '_2327.CylindricalGearSetSystemDeflectionWithLTCAResults':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSetSystemDeflectionWithLTCAResults
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2327.CylindricalGearSetSystemDeflectionWithLTCAResults)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2004.SpiralBevelGear') -> '_2352.SpiralBevelGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpiralBevelGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2352.SpiralBevelGearSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_2353.SpiralBevelGearLoadCase') -> '_2352.SpiralBevelGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpiralBevelGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2352.SpiralBevelGearSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_1966.SpiralBevelGearSet') -> '_2354.SpiralBevelGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpiralBevelGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2354.SpiralBevelGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_2355.SpiralBevelGearSetLoadCase') -> '_2354.SpiralBevelGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.SpiralBevelGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2354.SpiralBevelGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2005.StraightBevelDiffGear') -> '_2356.StraightBevelDiffGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelDiffGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2356.StraightBevelDiffGearSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_2357.StraightBevelDiffGearLoadCase') -> '_2356.StraightBevelDiffGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelDiffGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2356.StraightBevelDiffGearSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_1982.StraightBevelDiffGearSet') -> '_2358.StraightBevelDiffGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelDiffGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2358.StraightBevelDiffGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_2359.StraightBevelDiffGearSetLoadCase') -> '_2358.StraightBevelDiffGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelDiffGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2358.StraightBevelDiffGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2006.StraightBevelGear') -> '_2360.StraightBevelGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2360.StraightBevelGearSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_2361.StraightBevelGearLoadCase') -> '_2360.StraightBevelGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2360.StraightBevelGearSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_1964.StraightBevelGearSet') -> '_2362.StraightBevelGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2362.StraightBevelGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_2363.StraightBevelGearSetLoadCase') -> '_2362.StraightBevelGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2362.StraightBevelGearSetSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2010.StraightBevelPlanetGear') -> '_2364.StraightBevelPlanetGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelPlanetGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2364.StraightBevelPlanetGearSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_2365.StraightBevelPlanetGearLoadCase') -> '_2364.StraightBevelPlanetGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelPlanetGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2364.StraightBevelPlanetGearSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2011.StraightBevelSunGear') -> '_2366.StraightBevelSunGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelSunGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2366.StraightBevelSunGearSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_2367.StraightBevelSunGearLoadCase') -> '_2366.StraightBevelSunGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.StraightBevelSunGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2366.StraightBevelSunGearSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_1998.WormGear') -> '_2368.WormGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.WormGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2368.WormGearSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_2369.WormGearLoadCase') -> '_2368.WormGearSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.WormGearSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_2368.WormGearSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_1970.WormGearSet') -> '_2167.WormGearSetSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.system_deflections.WormGearSetSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_2167.WormGearSetSystemDeflection)(method_result) if method_result else None
