'''_2157.py

DynamicAnalysisAnalysis
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6211, _6212, _6214, _6158,
    _6157, _6056, _6069, _6068,
    _6074, _6073, _6087, _6086,
    _6089, _6090, _6167, _6173,
    _6171, _6169, _6183, _6182,
    _6194, _6193, _6195, _6196,
    _6200, _6201, _6202, _6088,
    _6055, _6070, _6083, _6138,
    _6159, _6170, _6175, _6058,
    _6076, _6114, _6186, _6063,
    _6080, _6050, _6093, _6134,
    _6140, _6143, _6146, _6179,
    _6189, _6210, _6213, _6120,
    _6156, _6067, _6072, _6085,
    _6181, _6199, _6046, _6047,
    _6054, _6066, _6065, _6071,
    _6084, _6099, _6112, _6116,
    _6053, _6124, _6136, _6148,
    _6149, _6151, _6153, _6155,
    _6162, _6165, _6166, _6172,
    _6176, _6207, _6208, _6174,
    _6075, _6077, _6113, _6115,
    _6049, _6051, _6057, _6059,
    _6060, _6061, _6062, _6064,
    _6078, _6082, _6091, _6095,
    _6096, _6118, _6123, _6133,
    _6135, _6139, _6141, _6142,
    _6144, _6145, _6147, _6160,
    _6178, _6180, _6185, _6187,
    _6188, _6190, _6191, _6192,
    _6209
)
from mastapy.system_model.analyses_and_results.dynamic_analyses import (
    _5914, _5915, _5917, _5872,
    _5873, _5803, _5815, _5816,
    _5820, _5821, _5831, _5832,
    _5834, _5835, _5879, _5885,
    _5882, _5880, _5892, _5893,
    _5902, _5903, _5904, _5905,
    _5907, _5908, _5909, _5833,
    _5802, _5817, _5828, _5856,
    _5874, _5881, _5886, _5805,
    _5823, _5845, _5895, _5810,
    _5826, _5798, _5837, _5853,
    _5858, _5861, _5864, _5889,
    _5898, _5913, _5916, _5849,
    _5871, _5814, _5819, _5830,
    _5891, _5906, _5795, _5796,
    _5801, _5812, _5813, _5818,
    _5829, _5840, _5843, _5847,
    _5800, _5851, _5855, _5866,
    _5867, _5868, _5869, _5870,
    _5876, _5877, _5878, _5883,
    _5887, _5910, _5911, _5884,
    _5822, _5824, _5844, _5846,
    _5797, _5799, _5804, _5806,
    _5807, _5808, _5809, _5811,
    _5825, _5827, _5836, _5838,
    _5839, _5848, _5850, _5852,
    _5854, _5857, _5859, _5860,
    _5862, _5863, _5865, _5875,
    _5888, _5890, _5894, _5896,
    _5897, _5899, _5900, _5901,
    _5912
)
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import (
    _2092, _2093, _2060, _2061,
    _2067, _2068, _2052, _2053,
    _2054, _2055, _2056, _2057,
    _2058, _2059, _2062, _2063,
    _2064, _2065, _2066, _2069,
    _2071, _2073, _2074, _2075,
    _2076, _2077, _2078, _2079,
    _2080, _2081, _2082, _2083,
    _2084, _2085, _2086, _2087,
    _2088, _2089, _2090, _2091
)
from mastapy.system_model.part_model.couplings import (
    _2122, _2123, _2111, _2113,
    _2114, _2116, _2117, _2118,
    _2119, _2120, _2121, _2124,
    _2132, _2130, _2131, _2133,
    _2134, _2135, _2137, _2138,
    _2139, _2140, _2141, _2143
)
from mastapy.system_model.connections_and_sockets import (
    _1837, _1832, _1833, _1836,
    _1845, _1848, _1852, _1856
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1862, _1866, _1872, _1886,
    _1864, _1868, _1860, _1870,
    _1876, _1879, _1880, _1881,
    _1884, _1888, _1890, _1892,
    _1874
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1900, _1894, _1896, _1898,
    _1902, _1904
)
from mastapy.system_model.part_model import (
    _1981, _1982, _1985, _1987,
    _1988, _1989, _1992, _1993,
    _1996, _1997, _1980, _1998,
    _2001, _2004, _2005, _2006,
    _2008, _2009, _2010, _2012,
    _2013, _2015, _2017, _2018,
    _2019
)
from mastapy.system_model.part_model.shaft_model import _2022
from mastapy.system_model.analyses_and_results import _2153
from mastapy._internal.python_net import python_net_import

_DYNAMIC_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'DynamicAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicAnalysisAnalysis',)


class DynamicAnalysisAnalysis(_2153.SingleAnalysis):
    '''DynamicAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _DYNAMIC_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DynamicAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6211.WormGearSetLoadCase') -> '_5914.WormGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5914.WormGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2092.ZerolBevelGear') -> '_5915.ZerolBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5915.ZerolBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6212.ZerolBevelGearLoadCase') -> '_5915.ZerolBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5915.ZerolBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2093.ZerolBevelGearSet') -> '_5917.ZerolBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5917.ZerolBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6214.ZerolBevelGearSetLoadCase') -> '_5917.ZerolBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5917.ZerolBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2122.PartToPartShearCoupling') -> '_5872.PartToPartShearCouplingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PartToPartShearCouplingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5872.PartToPartShearCouplingDynamicAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6158.PartToPartShearCouplingLoadCase') -> '_5872.PartToPartShearCouplingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PartToPartShearCouplingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5872.PartToPartShearCouplingDynamicAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2123.PartToPartShearCouplingHalf') -> '_5873.PartToPartShearCouplingHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PartToPartShearCouplingHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5873.PartToPartShearCouplingHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6157.PartToPartShearCouplingHalfLoadCase') -> '_5873.PartToPartShearCouplingHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PartToPartShearCouplingHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5873.PartToPartShearCouplingHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2111.BeltDrive') -> '_5803.BeltDriveDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BeltDriveDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5803.BeltDriveDynamicAnalysis)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6056.BeltDriveLoadCase') -> '_5803.BeltDriveDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BeltDriveDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5803.BeltDriveDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2113.Clutch') -> '_5815.ClutchDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5815.ClutchDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6069.ClutchLoadCase') -> '_5815.ClutchDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5815.ClutchDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2114.ClutchHalf') -> '_5816.ClutchHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5816.ClutchHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6068.ClutchHalfLoadCase') -> '_5816.ClutchHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5816.ClutchHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2116.ConceptCoupling') -> '_5820.ConceptCouplingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5820.ConceptCouplingDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6074.ConceptCouplingLoadCase') -> '_5820.ConceptCouplingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5820.ConceptCouplingDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2117.ConceptCouplingHalf') -> '_5821.ConceptCouplingHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5821.ConceptCouplingHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6073.ConceptCouplingHalfLoadCase') -> '_5821.ConceptCouplingHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5821.ConceptCouplingHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2118.Coupling') -> '_5831.CouplingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5831.CouplingDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6087.CouplingLoadCase') -> '_5831.CouplingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5831.CouplingDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2119.CouplingHalf') -> '_5832.CouplingHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5832.CouplingHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6086.CouplingHalfLoadCase') -> '_5832.CouplingHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5832.CouplingHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2120.CVT') -> '_5834.CVTDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5834.CVTDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6089.CVTLoadCase') -> '_5834.CVTDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5834.CVTDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2121.CVTPulley') -> '_5835.CVTPulleyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTPulleyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5835.CVTPulleyDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6090.CVTPulleyLoadCase') -> '_5835.CVTPulleyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTPulleyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5835.CVTPulleyDynamicAnalysis)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2124.Pulley') -> '_5879.PulleyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PulleyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5879.PulleyDynamicAnalysis)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6167.PulleyLoadCase') -> '_5879.PulleyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PulleyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5879.PulleyDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2132.ShaftHubConnection') -> '_5885.ShaftHubConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftHubConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5885.ShaftHubConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6173.ShaftHubConnectionLoadCase') -> '_5885.ShaftHubConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftHubConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5885.ShaftHubConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2130.RollingRing') -> '_5882.RollingRingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5882.RollingRingDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6171.RollingRingLoadCase') -> '_5882.RollingRingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5882.RollingRingDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2131.RollingRingAssembly') -> '_5880.RollingRingAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5880.RollingRingAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6169.RollingRingAssemblyLoadCase') -> '_5880.RollingRingAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5880.RollingRingAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2133.SpringDamper') -> '_5892.SpringDamperDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5892.SpringDamperDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6183.SpringDamperLoadCase') -> '_5892.SpringDamperDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5892.SpringDamperDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2134.SpringDamperHalf') -> '_5893.SpringDamperHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5893.SpringDamperHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6182.SpringDamperHalfLoadCase') -> '_5893.SpringDamperHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5893.SpringDamperHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2135.Synchroniser') -> '_5902.SynchroniserDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5902.SynchroniserDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6194.SynchroniserLoadCase') -> '_5902.SynchroniserDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5902.SynchroniserDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2137.SynchroniserHalf') -> '_5903.SynchroniserHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5903.SynchroniserHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6193.SynchroniserHalfLoadCase') -> '_5903.SynchroniserHalfDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserHalfDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5903.SynchroniserHalfDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2138.SynchroniserPart') -> '_5904.SynchroniserPartDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserPartDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5904.SynchroniserPartDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6195.SynchroniserPartLoadCase') -> '_5904.SynchroniserPartDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserPartDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5904.SynchroniserPartDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2139.SynchroniserSleeve') -> '_5905.SynchroniserSleeveDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserSleeveDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5905.SynchroniserSleeveDynamicAnalysis)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6196.SynchroniserSleeveLoadCase') -> '_5905.SynchroniserSleeveDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SynchroniserSleeveDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5905.SynchroniserSleeveDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2140.TorqueConverter') -> '_5907.TorqueConverterDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5907.TorqueConverterDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6200.TorqueConverterLoadCase') -> '_5907.TorqueConverterDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5907.TorqueConverterDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2141.TorqueConverterPump') -> '_5908.TorqueConverterPumpDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterPumpDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5908.TorqueConverterPumpDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6201.TorqueConverterPumpLoadCase') -> '_5908.TorqueConverterPumpDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterPumpDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5908.TorqueConverterPumpDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2143.TorqueConverterTurbine') -> '_5909.TorqueConverterTurbineDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterTurbineDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5909.TorqueConverterTurbineDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6202.TorqueConverterTurbineLoadCase') -> '_5909.TorqueConverterTurbineDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterTurbineDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5909.TorqueConverterTurbineDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1837.CVTBeltConnection') -> '_5833.CVTBeltConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTBeltConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5833.CVTBeltConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6088.CVTBeltConnectionLoadCase') -> '_5833.CVTBeltConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CVTBeltConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5833.CVTBeltConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1832.BeltConnection') -> '_5802.BeltConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BeltConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5802.BeltConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6055.BeltConnectionLoadCase') -> '_5802.BeltConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BeltConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5802.BeltConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1833.CoaxialConnection') -> '_5817.CoaxialConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CoaxialConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5817.CoaxialConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6070.CoaxialConnectionLoadCase') -> '_5817.CoaxialConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CoaxialConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5817.CoaxialConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1836.Connection') -> '_5828.ConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5828.ConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6083.ConnectionLoadCase') -> '_5828.ConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5828.ConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1845.InterMountableComponentConnection') -> '_5856.InterMountableComponentConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.InterMountableComponentConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5856.InterMountableComponentConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6138.InterMountableComponentConnectionLoadCase') -> '_5856.InterMountableComponentConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.InterMountableComponentConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5856.InterMountableComponentConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1848.PlanetaryConnection') -> '_5874.PlanetaryConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetaryConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5874.PlanetaryConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6159.PlanetaryConnectionLoadCase') -> '_5874.PlanetaryConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetaryConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5874.PlanetaryConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1852.RollingRingConnection') -> '_5881.RollingRingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5881.RollingRingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6170.RollingRingConnectionLoadCase') -> '_5881.RollingRingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RollingRingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5881.RollingRingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1856.ShaftToMountableComponentConnection') -> '_5886.ShaftToMountableComponentConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftToMountableComponentConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5886.ShaftToMountableComponentConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6175.ShaftToMountableComponentConnectionLoadCase') -> '_5886.ShaftToMountableComponentConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftToMountableComponentConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5886.ShaftToMountableComponentConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1862.BevelDifferentialGearMesh') -> '_5805.BevelDifferentialGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5805.BevelDifferentialGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6058.BevelDifferentialGearMeshLoadCase') -> '_5805.BevelDifferentialGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5805.BevelDifferentialGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1866.ConceptGearMesh') -> '_5823.ConceptGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5823.ConceptGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6076.ConceptGearMeshLoadCase') -> '_5823.ConceptGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5823.ConceptGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1872.FaceGearMesh') -> '_5845.FaceGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5845.FaceGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6114.FaceGearMeshLoadCase') -> '_5845.FaceGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5845.FaceGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1886.StraightBevelDiffGearMesh') -> '_5895.StraightBevelDiffGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5895.StraightBevelDiffGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6186.StraightBevelDiffGearMeshLoadCase') -> '_5895.StraightBevelDiffGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5895.StraightBevelDiffGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1864.BevelGearMesh') -> '_5810.BevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5810.BevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6063.BevelGearMeshLoadCase') -> '_5810.BevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5810.BevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1868.ConicalGearMesh') -> '_5826.ConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5826.ConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6080.ConicalGearMeshLoadCase') -> '_5826.ConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5826.ConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1860.AGMAGleasonConicalGearMesh') -> '_5798.AGMAGleasonConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5798.AGMAGleasonConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6050.AGMAGleasonConicalGearMeshLoadCase') -> '_5798.AGMAGleasonConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5798.AGMAGleasonConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1870.CylindricalGearMesh') -> '_5837.CylindricalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5837.CylindricalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6093.CylindricalGearMeshLoadCase') -> '_5837.CylindricalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5837.CylindricalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1876.HypoidGearMesh') -> '_5853.HypoidGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5853.HypoidGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6134.HypoidGearMeshLoadCase') -> '_5853.HypoidGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5853.HypoidGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidConicalGearMesh') -> '_5858.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5858.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6140.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_5858.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5858.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1880.KlingelnbergCycloPalloidHypoidGearMesh') -> '_5861.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5861.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6143.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_5861.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5861.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1881.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_5864.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5864.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6146.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_5864.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5864.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1884.SpiralBevelGearMesh') -> '_5889.SpiralBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5889.SpiralBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6179.SpiralBevelGearMeshLoadCase') -> '_5889.SpiralBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5889.SpiralBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1888.StraightBevelGearMesh') -> '_5898.StraightBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5898.StraightBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6189.StraightBevelGearMeshLoadCase') -> '_5898.StraightBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5898.StraightBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1890.WormGearMesh') -> '_5913.WormGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5913.WormGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6210.WormGearMeshLoadCase') -> '_5913.WormGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5913.WormGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1892.ZerolBevelGearMesh') -> '_5916.ZerolBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5916.ZerolBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6213.ZerolBevelGearMeshLoadCase') -> '_5916.ZerolBevelGearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ZerolBevelGearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5916.ZerolBevelGearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1874.GearMesh') -> '_5849.GearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5849.GearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6120.GearMeshLoadCase') -> '_5849.GearMeshDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearMeshDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5849.GearMeshDynamicAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1900.PartToPartShearCouplingConnection') -> '_5871.PartToPartShearCouplingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PartToPartShearCouplingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5871.PartToPartShearCouplingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6156.PartToPartShearCouplingConnectionLoadCase') -> '_5871.PartToPartShearCouplingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PartToPartShearCouplingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5871.PartToPartShearCouplingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1894.ClutchConnection') -> '_5814.ClutchConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5814.ClutchConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6067.ClutchConnectionLoadCase') -> '_5814.ClutchConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ClutchConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5814.ClutchConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1896.ConceptCouplingConnection') -> '_5819.ConceptCouplingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5819.ConceptCouplingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6072.ConceptCouplingConnectionLoadCase') -> '_5819.ConceptCouplingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptCouplingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5819.ConceptCouplingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1898.CouplingConnection') -> '_5830.CouplingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5830.CouplingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6085.CouplingConnectionLoadCase') -> '_5830.CouplingConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5830.CouplingConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1902.SpringDamperConnection') -> '_5891.SpringDamperConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5891.SpringDamperConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6181.SpringDamperConnectionLoadCase') -> '_5891.SpringDamperConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpringDamperConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5891.SpringDamperConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1904.TorqueConverterConnection') -> '_5906.TorqueConverterConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5906.TorqueConverterConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6199.TorqueConverterConnectionLoadCase') -> '_5906.TorqueConverterConnectionDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.TorqueConverterConnectionDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5906.TorqueConverterConnectionDynamicAnalysis)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1981.AbstractAssembly') -> '_5795.AbstractAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AbstractAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5795.AbstractAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6046.AbstractAssemblyLoadCase') -> '_5795.AbstractAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AbstractAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5795.AbstractAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1982.AbstractShaftOrHousing') -> '_5796.AbstractShaftOrHousingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AbstractShaftOrHousingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5796.AbstractShaftOrHousingDynamicAnalysis)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6047.AbstractShaftOrHousingLoadCase') -> '_5796.AbstractShaftOrHousingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AbstractShaftOrHousingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5796.AbstractShaftOrHousingDynamicAnalysis)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1985.Bearing') -> '_5801.BearingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BearingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5801.BearingDynamicAnalysis)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6054.BearingLoadCase') -> '_5801.BearingDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BearingDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5801.BearingDynamicAnalysis)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1987.Bolt') -> '_5812.BoltDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BoltDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5812.BoltDynamicAnalysis)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6066.BoltLoadCase') -> '_5812.BoltDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BoltDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5812.BoltDynamicAnalysis)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1988.BoltedJoint') -> '_5813.BoltedJointDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BoltedJointDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5813.BoltedJointDynamicAnalysis)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6065.BoltedJointLoadCase') -> '_5813.BoltedJointDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BoltedJointDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5813.BoltedJointDynamicAnalysis)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1989.Component') -> '_5818.ComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5818.ComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6071.ComponentLoadCase') -> '_5818.ComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5818.ComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1992.Connector') -> '_5829.ConnectorDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConnectorDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5829.ConnectorDynamicAnalysis)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6084.ConnectorLoadCase') -> '_5829.ConnectorDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConnectorDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5829.ConnectorDynamicAnalysis)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1993.Datum') -> '_5840.DatumDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.DatumDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5840.DatumDynamicAnalysis)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6099.DatumLoadCase') -> '_5840.DatumDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.DatumDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5840.DatumDynamicAnalysis)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1996.ExternalCADModel') -> '_5843.ExternalCADModelDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ExternalCADModelDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5843.ExternalCADModelDynamicAnalysis)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6112.ExternalCADModelLoadCase') -> '_5843.ExternalCADModelDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ExternalCADModelDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5843.ExternalCADModelDynamicAnalysis)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1997.FlexiblePinAssembly') -> '_5847.FlexiblePinAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FlexiblePinAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5847.FlexiblePinAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6116.FlexiblePinAssemblyLoadCase') -> '_5847.FlexiblePinAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FlexiblePinAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5847.FlexiblePinAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1980.Assembly') -> '_5800.AssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5800.AssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6053.AssemblyLoadCase') -> '_5800.AssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5800.AssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1998.GuideDxfModel') -> '_5851.GuideDxfModelDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GuideDxfModelDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5851.GuideDxfModelDynamicAnalysis)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6124.GuideDxfModelLoadCase') -> '_5851.GuideDxfModelDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GuideDxfModelDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5851.GuideDxfModelDynamicAnalysis)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_2001.ImportedFEComponent') -> '_5855.ImportedFEComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ImportedFEComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5855.ImportedFEComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_6136.ImportedFEComponentLoadCase') -> '_5855.ImportedFEComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ImportedFEComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5855.ImportedFEComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_2004.MassDisc') -> '_5866.MassDiscDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MassDiscDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5866.MassDiscDynamicAnalysis)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6148.MassDiscLoadCase') -> '_5866.MassDiscDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MassDiscDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5866.MassDiscDynamicAnalysis)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_2005.MeasurementComponent') -> '_5867.MeasurementComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MeasurementComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5867.MeasurementComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6149.MeasurementComponentLoadCase') -> '_5867.MeasurementComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MeasurementComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5867.MeasurementComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_2006.MountableComponent') -> '_5868.MountableComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MountableComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5868.MountableComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6151.MountableComponentLoadCase') -> '_5868.MountableComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.MountableComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5868.MountableComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_2008.OilSeal') -> '_5869.OilSealDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.OilSealDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5869.OilSealDynamicAnalysis)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6153.OilSealLoadCase') -> '_5869.OilSealDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.OilSealDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5869.OilSealDynamicAnalysis)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_2009.Part') -> '_5870.PartDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PartDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5870.PartDynamicAnalysis)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6155.PartLoadCase') -> '_5870.PartDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PartDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5870.PartDynamicAnalysis)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_2010.PlanetCarrier') -> '_5876.PlanetCarrierDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetCarrierDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5876.PlanetCarrierDynamicAnalysis)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6162.PlanetCarrierLoadCase') -> '_5876.PlanetCarrierDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetCarrierDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5876.PlanetCarrierDynamicAnalysis)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_2012.PointLoad') -> '_5877.PointLoadDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PointLoadDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5877.PointLoadDynamicAnalysis)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6165.PointLoadLoadCase') -> '_5877.PointLoadDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PointLoadDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5877.PointLoadDynamicAnalysis)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_2013.PowerLoad') -> '_5878.PowerLoadDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PowerLoadDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5878.PowerLoadDynamicAnalysis)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6166.PowerLoadLoadCase') -> '_5878.PowerLoadDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PowerLoadDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5878.PowerLoadDynamicAnalysis)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_2015.RootAssembly') -> '_5883.RootAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RootAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5883.RootAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6172.RootAssemblyLoadCase') -> '_5883.RootAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.RootAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5883.RootAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_2017.SpecialisedAssembly') -> '_5887.SpecialisedAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpecialisedAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5887.SpecialisedAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6176.SpecialisedAssemblyLoadCase') -> '_5887.SpecialisedAssemblyDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpecialisedAssemblyDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5887.SpecialisedAssemblyDynamicAnalysis)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_2018.UnbalancedMass') -> '_5910.UnbalancedMassDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.UnbalancedMassDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5910.UnbalancedMassDynamicAnalysis)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6207.UnbalancedMassLoadCase') -> '_5910.UnbalancedMassDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.UnbalancedMassDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5910.UnbalancedMassDynamicAnalysis)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_2019.VirtualComponent') -> '_5911.VirtualComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.VirtualComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5911.VirtualComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6208.VirtualComponentLoadCase') -> '_5911.VirtualComponentDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.VirtualComponentDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5911.VirtualComponentDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_2022.Shaft') -> '_5884.ShaftDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5884.ShaftDynamicAnalysis)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6174.ShaftLoadCase') -> '_5884.ShaftDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ShaftDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5884.ShaftDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2060.ConceptGear') -> '_5822.ConceptGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5822.ConceptGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6075.ConceptGearLoadCase') -> '_5822.ConceptGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5822.ConceptGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2061.ConceptGearSet') -> '_5824.ConceptGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5824.ConceptGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6077.ConceptGearSetLoadCase') -> '_5824.ConceptGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConceptGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5824.ConceptGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2067.FaceGear') -> '_5844.FaceGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5844.FaceGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6113.FaceGearLoadCase') -> '_5844.FaceGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5844.FaceGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2068.FaceGearSet') -> '_5846.FaceGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5846.FaceGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6115.FaceGearSetLoadCase') -> '_5846.FaceGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.FaceGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5846.FaceGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2052.AGMAGleasonConicalGear') -> '_5797.AGMAGleasonConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5797.AGMAGleasonConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6049.AGMAGleasonConicalGearLoadCase') -> '_5797.AGMAGleasonConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5797.AGMAGleasonConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2053.AGMAGleasonConicalGearSet') -> '_5799.AGMAGleasonConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5799.AGMAGleasonConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6051.AGMAGleasonConicalGearSetLoadCase') -> '_5799.AGMAGleasonConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5799.AGMAGleasonConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2054.BevelDifferentialGear') -> '_5804.BevelDifferentialGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5804.BevelDifferentialGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6057.BevelDifferentialGearLoadCase') -> '_5804.BevelDifferentialGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5804.BevelDifferentialGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2055.BevelDifferentialGearSet') -> '_5806.BevelDifferentialGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5806.BevelDifferentialGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6059.BevelDifferentialGearSetLoadCase') -> '_5806.BevelDifferentialGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5806.BevelDifferentialGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2056.BevelDifferentialPlanetGear') -> '_5807.BevelDifferentialPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5807.BevelDifferentialPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6060.BevelDifferentialPlanetGearLoadCase') -> '_5807.BevelDifferentialPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5807.BevelDifferentialPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2057.BevelDifferentialSunGear') -> '_5808.BevelDifferentialSunGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialSunGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5808.BevelDifferentialSunGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6061.BevelDifferentialSunGearLoadCase') -> '_5808.BevelDifferentialSunGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelDifferentialSunGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5808.BevelDifferentialSunGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2058.BevelGear') -> '_5809.BevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5809.BevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6062.BevelGearLoadCase') -> '_5809.BevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5809.BevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2059.BevelGearSet') -> '_5811.BevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5811.BevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6064.BevelGearSetLoadCase') -> '_5811.BevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5811.BevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2062.ConicalGear') -> '_5825.ConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5825.ConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6078.ConicalGearLoadCase') -> '_5825.ConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5825.ConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2063.ConicalGearSet') -> '_5827.ConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5827.ConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6082.ConicalGearSetLoadCase') -> '_5827.ConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.ConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5827.ConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2064.CylindricalGear') -> '_5836.CylindricalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5836.CylindricalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6091.CylindricalGearLoadCase') -> '_5836.CylindricalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5836.CylindricalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2065.CylindricalGearSet') -> '_5838.CylindricalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5838.CylindricalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6095.CylindricalGearSetLoadCase') -> '_5838.CylindricalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5838.CylindricalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2066.CylindricalPlanetGear') -> '_5839.CylindricalPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5839.CylindricalPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6096.CylindricalPlanetGearLoadCase') -> '_5839.CylindricalPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5839.CylindricalPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2069.Gear') -> '_5848.GearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5848.GearDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6118.GearLoadCase') -> '_5848.GearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5848.GearDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2071.GearSet') -> '_5850.GearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5850.GearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6123.GearSetLoadCase') -> '_5850.GearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.GearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5850.GearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2073.HypoidGear') -> '_5852.HypoidGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5852.HypoidGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6133.HypoidGearLoadCase') -> '_5852.HypoidGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5852.HypoidGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2074.HypoidGearSet') -> '_5854.HypoidGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5854.HypoidGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6135.HypoidGearSetLoadCase') -> '_5854.HypoidGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5854.HypoidGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2075.KlingelnbergCycloPalloidConicalGear') -> '_5857.KlingelnbergCycloPalloidConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5857.KlingelnbergCycloPalloidConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6139.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_5857.KlingelnbergCycloPalloidConicalGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5857.KlingelnbergCycloPalloidConicalGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2076.KlingelnbergCycloPalloidConicalGearSet') -> '_5859.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5859.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6141.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_5859.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5859.KlingelnbergCycloPalloidConicalGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2077.KlingelnbergCycloPalloidHypoidGear') -> '_5860.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5860.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6142.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_5860.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5860.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2078.KlingelnbergCycloPalloidHypoidGearSet') -> '_5862.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5862.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6144.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_5862.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5862.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2079.KlingelnbergCycloPalloidSpiralBevelGear') -> '_5863.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5863.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6145.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_5863.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5863.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2080.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_5865.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5865.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6147.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_5865.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5865.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2081.PlanetaryGearSet') -> '_5875.PlanetaryGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetaryGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5875.PlanetaryGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6160.PlanetaryGearSetLoadCase') -> '_5875.PlanetaryGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.PlanetaryGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5875.PlanetaryGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2082.SpiralBevelGear') -> '_5888.SpiralBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5888.SpiralBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6178.SpiralBevelGearLoadCase') -> '_5888.SpiralBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5888.SpiralBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2083.SpiralBevelGearSet') -> '_5890.SpiralBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5890.SpiralBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6180.SpiralBevelGearSetLoadCase') -> '_5890.SpiralBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.SpiralBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5890.SpiralBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2084.StraightBevelDiffGear') -> '_5894.StraightBevelDiffGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5894.StraightBevelDiffGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6185.StraightBevelDiffGearLoadCase') -> '_5894.StraightBevelDiffGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5894.StraightBevelDiffGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2085.StraightBevelDiffGearSet') -> '_5896.StraightBevelDiffGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5896.StraightBevelDiffGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6187.StraightBevelDiffGearSetLoadCase') -> '_5896.StraightBevelDiffGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5896.StraightBevelDiffGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2086.StraightBevelGear') -> '_5897.StraightBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5897.StraightBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6188.StraightBevelGearLoadCase') -> '_5897.StraightBevelGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5897.StraightBevelGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2087.StraightBevelGearSet') -> '_5899.StraightBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5899.StraightBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6190.StraightBevelGearSetLoadCase') -> '_5899.StraightBevelGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5899.StraightBevelGearSetDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2088.StraightBevelPlanetGear') -> '_5900.StraightBevelPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5900.StraightBevelPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6191.StraightBevelPlanetGearLoadCase') -> '_5900.StraightBevelPlanetGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelPlanetGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5900.StraightBevelPlanetGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2089.StraightBevelSunGear') -> '_5901.StraightBevelSunGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelSunGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5901.StraightBevelSunGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6192.StraightBevelSunGearLoadCase') -> '_5901.StraightBevelSunGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelSunGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5901.StraightBevelSunGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2090.WormGear') -> '_5912.WormGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5912.WormGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6209.WormGearLoadCase') -> '_5912.WormGearDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_5912.WormGearDynamicAnalysis)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2091.WormGearSet') -> '_5914.WormGearSetDynamicAnalysis':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.dynamic_analyses.WormGearSetDynamicAnalysis
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_5914.WormGearSetDynamicAnalysis)(method_result) if method_result else None
