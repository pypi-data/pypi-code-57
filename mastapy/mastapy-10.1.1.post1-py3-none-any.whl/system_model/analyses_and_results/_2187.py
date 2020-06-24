'''_2187.py

CompoundDynamicAnalysisAnalysis
'''


from typing import Iterable

from mastapy.system_model.part_model import (
    _1981, _1982, _1985, _1987,
    _1988, _1989, _1992, _1993,
    _1996, _1997, _1980, _1998,
    _2001, _2004, _2005, _2006,
    _2008, _2009, _2010, _2012,
    _2013, _2015, _2017, _2018,
    _2019
)
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import (
    _5918, _5919, _5924, _5935,
    _5936, _5941, _5952, _5963,
    _5964, _5968, _5923, _5972,
    _5976, _5987, _5988, _5989,
    _5990, _5991, _5997, _5998,
    _5999, _6004, _6008, _6031,
    _6032, _6005, _5945, _5947,
    _5965, _5967, _5920, _5922,
    _5927, _5929, _5930, _5931,
    _5932, _5934, _5948, _5950,
    _5959, _5961, _5962, _5969,
    _5971, _5973, _5975, _5978,
    _5980, _5981, _5983, _5984,
    _5986, _5996, _6009, _6011,
    _6015, _6017, _6018, _6020,
    _6021, _6022, _6033, _6035,
    _6036, _6038, _5992, _5994,
    _5926, _5937, _5939, _5942,
    _5944, _5953, _5955, _5957,
    _5958, _6000, _6006, _6002,
    _6001, _6012, _6014, _6023,
    _6024, _6025, _6026, _6027,
    _6029, _6030, _5956, _5925,
    _5940, _5951, _5977, _5995,
    _6003, _6007, _5928, _5946,
    _5966, _6016, _5933, _5949,
    _5921, _5960, _5974, _5979,
    _5982, _5985, _6010, _6019,
    _6034, _6037, _5970, _5993,
    _5938, _5943, _5954, _6013,
    _6028
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2022
from mastapy.system_model.part_model.gears import (
    _2060, _2061, _2067, _2068,
    _2052, _2053, _2054, _2055,
    _2056, _2057, _2058, _2059,
    _2062, _2063, _2064, _2065,
    _2066, _2069, _2071, _2073,
    _2074, _2075, _2076, _2077,
    _2078, _2079, _2080, _2081,
    _2082, _2083, _2084, _2085,
    _2086, _2087, _2088, _2089,
    _2090, _2091, _2092, _2093
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
from mastapy.system_model.analyses_and_results import _2152
from mastapy._internal.python_net import python_net_import

_COMPOUND_DYNAMIC_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundDynamicAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundDynamicAnalysisAnalysis',)


class CompoundDynamicAnalysisAnalysis(_2152.CompoundAnalysis):
    '''CompoundDynamicAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_DYNAMIC_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundDynamicAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1981.AbstractAssembly') -> 'Iterable[_5918.AbstractAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AbstractAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5918.AbstractAssemblyCompoundDynamicAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1982.AbstractShaftOrHousing') -> 'Iterable[_5919.AbstractShaftOrHousingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AbstractShaftOrHousingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5919.AbstractShaftOrHousingCompoundDynamicAnalysis))

    def results_for_bearing(self, design_entity: '_1985.Bearing') -> 'Iterable[_5924.BearingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BearingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5924.BearingCompoundDynamicAnalysis))

    def results_for_bolt(self, design_entity: '_1987.Bolt') -> 'Iterable[_5935.BoltCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BoltCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5935.BoltCompoundDynamicAnalysis))

    def results_for_bolted_joint(self, design_entity: '_1988.BoltedJoint') -> 'Iterable[_5936.BoltedJointCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BoltedJointCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5936.BoltedJointCompoundDynamicAnalysis))

    def results_for_component(self, design_entity: '_1989.Component') -> 'Iterable[_5941.ComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5941.ComponentCompoundDynamicAnalysis))

    def results_for_connector(self, design_entity: '_1992.Connector') -> 'Iterable[_5952.ConnectorCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConnectorCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5952.ConnectorCompoundDynamicAnalysis))

    def results_for_datum(self, design_entity: '_1993.Datum') -> 'Iterable[_5963.DatumCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.DatumCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5963.DatumCompoundDynamicAnalysis))

    def results_for_external_cad_model(self, design_entity: '_1996.ExternalCADModel') -> 'Iterable[_5964.ExternalCADModelCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ExternalCADModelCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5964.ExternalCADModelCompoundDynamicAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_1997.FlexiblePinAssembly') -> 'Iterable[_5968.FlexiblePinAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FlexiblePinAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5968.FlexiblePinAssemblyCompoundDynamicAnalysis))

    def results_for_assembly(self, design_entity: '_1980.Assembly') -> 'Iterable[_5923.AssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5923.AssemblyCompoundDynamicAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_1998.GuideDxfModel') -> 'Iterable[_5972.GuideDxfModelCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GuideDxfModelCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5972.GuideDxfModelCompoundDynamicAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_2001.ImportedFEComponent') -> 'Iterable[_5976.ImportedFEComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ImportedFEComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5976.ImportedFEComponentCompoundDynamicAnalysis))

    def results_for_mass_disc(self, design_entity: '_2004.MassDisc') -> 'Iterable[_5987.MassDiscCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MassDiscCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5987.MassDiscCompoundDynamicAnalysis))

    def results_for_measurement_component(self, design_entity: '_2005.MeasurementComponent') -> 'Iterable[_5988.MeasurementComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MeasurementComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5988.MeasurementComponentCompoundDynamicAnalysis))

    def results_for_mountable_component(self, design_entity: '_2006.MountableComponent') -> 'Iterable[_5989.MountableComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MountableComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5989.MountableComponentCompoundDynamicAnalysis))

    def results_for_oil_seal(self, design_entity: '_2008.OilSeal') -> 'Iterable[_5990.OilSealCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.OilSealCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5990.OilSealCompoundDynamicAnalysis))

    def results_for_part(self, design_entity: '_2009.Part') -> 'Iterable[_5991.PartCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5991.PartCompoundDynamicAnalysis))

    def results_for_planet_carrier(self, design_entity: '_2010.PlanetCarrier') -> 'Iterable[_5997.PlanetCarrierCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetCarrierCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5997.PlanetCarrierCompoundDynamicAnalysis))

    def results_for_point_load(self, design_entity: '_2012.PointLoad') -> 'Iterable[_5998.PointLoadCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PointLoadCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5998.PointLoadCompoundDynamicAnalysis))

    def results_for_power_load(self, design_entity: '_2013.PowerLoad') -> 'Iterable[_5999.PowerLoadCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PowerLoadCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5999.PowerLoadCompoundDynamicAnalysis))

    def results_for_root_assembly(self, design_entity: '_2015.RootAssembly') -> 'Iterable[_6004.RootAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RootAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6004.RootAssemblyCompoundDynamicAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_2017.SpecialisedAssembly') -> 'Iterable[_6008.SpecialisedAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpecialisedAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6008.SpecialisedAssemblyCompoundDynamicAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_2018.UnbalancedMass') -> 'Iterable[_6031.UnbalancedMassCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.UnbalancedMassCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6031.UnbalancedMassCompoundDynamicAnalysis))

    def results_for_virtual_component(self, design_entity: '_2019.VirtualComponent') -> 'Iterable[_6032.VirtualComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.VirtualComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6032.VirtualComponentCompoundDynamicAnalysis))

    def results_for_shaft(self, design_entity: '_2022.Shaft') -> 'Iterable[_6005.ShaftCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6005.ShaftCompoundDynamicAnalysis))

    def results_for_concept_gear(self, design_entity: '_2060.ConceptGear') -> 'Iterable[_5945.ConceptGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5945.ConceptGearCompoundDynamicAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_2061.ConceptGearSet') -> 'Iterable[_5947.ConceptGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5947.ConceptGearSetCompoundDynamicAnalysis))

    def results_for_face_gear(self, design_entity: '_2067.FaceGear') -> 'Iterable[_5965.FaceGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5965.FaceGearCompoundDynamicAnalysis))

    def results_for_face_gear_set(self, design_entity: '_2068.FaceGearSet') -> 'Iterable[_5967.FaceGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5967.FaceGearSetCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2052.AGMAGleasonConicalGear') -> 'Iterable[_5920.AGMAGleasonConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5920.AGMAGleasonConicalGearCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2053.AGMAGleasonConicalGearSet') -> 'Iterable[_5922.AGMAGleasonConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5922.AGMAGleasonConicalGearSetCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2054.BevelDifferentialGear') -> 'Iterable[_5927.BevelDifferentialGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5927.BevelDifferentialGearCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2055.BevelDifferentialGearSet') -> 'Iterable[_5929.BevelDifferentialGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5929.BevelDifferentialGearSetCompoundDynamicAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2056.BevelDifferentialPlanetGear') -> 'Iterable[_5930.BevelDifferentialPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5930.BevelDifferentialPlanetGearCompoundDynamicAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2057.BevelDifferentialSunGear') -> 'Iterable[_5931.BevelDifferentialSunGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialSunGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5931.BevelDifferentialSunGearCompoundDynamicAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2058.BevelGear') -> 'Iterable[_5932.BevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5932.BevelGearCompoundDynamicAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_2059.BevelGearSet') -> 'Iterable[_5934.BevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5934.BevelGearSetCompoundDynamicAnalysis))

    def results_for_conical_gear(self, design_entity: '_2062.ConicalGear') -> 'Iterable[_5948.ConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5948.ConicalGearCompoundDynamicAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_2063.ConicalGearSet') -> 'Iterable[_5950.ConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5950.ConicalGearSetCompoundDynamicAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_2064.CylindricalGear') -> 'Iterable[_5959.CylindricalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5959.CylindricalGearCompoundDynamicAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_2065.CylindricalGearSet') -> 'Iterable[_5961.CylindricalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5961.CylindricalGearSetCompoundDynamicAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2066.CylindricalPlanetGear') -> 'Iterable[_5962.CylindricalPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5962.CylindricalPlanetGearCompoundDynamicAnalysis))

    def results_for_gear(self, design_entity: '_2069.Gear') -> 'Iterable[_5969.GearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5969.GearCompoundDynamicAnalysis))

    def results_for_gear_set(self, design_entity: '_2071.GearSet') -> 'Iterable[_5971.GearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5971.GearSetCompoundDynamicAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2073.HypoidGear') -> 'Iterable[_5973.HypoidGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5973.HypoidGearCompoundDynamicAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_2074.HypoidGearSet') -> 'Iterable[_5975.HypoidGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5975.HypoidGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2075.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_5978.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5978.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2076.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_5980.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5980.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2077.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_5981.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5981.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2078.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_5983.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5983.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2079.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_5984.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5984.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2080.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_5986.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5986.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_2081.PlanetaryGearSet') -> 'Iterable[_5996.PlanetaryGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetaryGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5996.PlanetaryGearSetCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2082.SpiralBevelGear') -> 'Iterable[_6009.SpiralBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6009.SpiralBevelGearCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2083.SpiralBevelGearSet') -> 'Iterable[_6011.SpiralBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6011.SpiralBevelGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2084.StraightBevelDiffGear') -> 'Iterable[_6015.StraightBevelDiffGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6015.StraightBevelDiffGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2085.StraightBevelDiffGearSet') -> 'Iterable[_6017.StraightBevelDiffGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6017.StraightBevelDiffGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2086.StraightBevelGear') -> 'Iterable[_6018.StraightBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6018.StraightBevelGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2087.StraightBevelGearSet') -> 'Iterable[_6020.StraightBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6020.StraightBevelGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2088.StraightBevelPlanetGear') -> 'Iterable[_6021.StraightBevelPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6021.StraightBevelPlanetGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2089.StraightBevelSunGear') -> 'Iterable[_6022.StraightBevelSunGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelSunGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6022.StraightBevelSunGearCompoundDynamicAnalysis))

    def results_for_worm_gear(self, design_entity: '_2090.WormGear') -> 'Iterable[_6033.WormGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6033.WormGearCompoundDynamicAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_2091.WormGearSet') -> 'Iterable[_6035.WormGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6035.WormGearSetCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2092.ZerolBevelGear') -> 'Iterable[_6036.ZerolBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6036.ZerolBevelGearCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2093.ZerolBevelGearSet') -> 'Iterable[_6038.ZerolBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6038.ZerolBevelGearSetCompoundDynamicAnalysis))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2122.PartToPartShearCoupling') -> 'Iterable[_5992.PartToPartShearCouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartToPartShearCouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5992.PartToPartShearCouplingCompoundDynamicAnalysis))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2123.PartToPartShearCouplingHalf') -> 'Iterable[_5994.PartToPartShearCouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartToPartShearCouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5994.PartToPartShearCouplingHalfCompoundDynamicAnalysis))

    def results_for_belt_drive(self, design_entity: '_2111.BeltDrive') -> 'Iterable[_5926.BeltDriveCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BeltDriveCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5926.BeltDriveCompoundDynamicAnalysis))

    def results_for_clutch(self, design_entity: '_2113.Clutch') -> 'Iterable[_5937.ClutchCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5937.ClutchCompoundDynamicAnalysis))

    def results_for_clutch_half(self, design_entity: '_2114.ClutchHalf') -> 'Iterable[_5939.ClutchHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5939.ClutchHalfCompoundDynamicAnalysis))

    def results_for_concept_coupling(self, design_entity: '_2116.ConceptCoupling') -> 'Iterable[_5942.ConceptCouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5942.ConceptCouplingCompoundDynamicAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2117.ConceptCouplingHalf') -> 'Iterable[_5944.ConceptCouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5944.ConceptCouplingHalfCompoundDynamicAnalysis))

    def results_for_coupling(self, design_entity: '_2118.Coupling') -> 'Iterable[_5953.CouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5953.CouplingCompoundDynamicAnalysis))

    def results_for_coupling_half(self, design_entity: '_2119.CouplingHalf') -> 'Iterable[_5955.CouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5955.CouplingHalfCompoundDynamicAnalysis))

    def results_for_cvt(self, design_entity: '_2120.CVT') -> 'Iterable[_5957.CVTCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5957.CVTCompoundDynamicAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2121.CVTPulley') -> 'Iterable[_5958.CVTPulleyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTPulleyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5958.CVTPulleyCompoundDynamicAnalysis))

    def results_for_pulley(self, design_entity: '_2124.Pulley') -> 'Iterable[_6000.PulleyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PulleyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6000.PulleyCompoundDynamicAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_2132.ShaftHubConnection') -> 'Iterable[_6006.ShaftHubConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftHubConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6006.ShaftHubConnectionCompoundDynamicAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2130.RollingRing') -> 'Iterable[_6002.RollingRingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6002.RollingRingCompoundDynamicAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_2131.RollingRingAssembly') -> 'Iterable[_6001.RollingRingAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6001.RollingRingAssemblyCompoundDynamicAnalysis))

    def results_for_spring_damper(self, design_entity: '_2133.SpringDamper') -> 'Iterable[_6012.SpringDamperCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6012.SpringDamperCompoundDynamicAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2134.SpringDamperHalf') -> 'Iterable[_6014.SpringDamperHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6014.SpringDamperHalfCompoundDynamicAnalysis))

    def results_for_synchroniser(self, design_entity: '_2135.Synchroniser') -> 'Iterable[_6023.SynchroniserCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6023.SynchroniserCompoundDynamicAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2137.SynchroniserHalf') -> 'Iterable[_6024.SynchroniserHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6024.SynchroniserHalfCompoundDynamicAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2138.SynchroniserPart') -> 'Iterable[_6025.SynchroniserPartCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserPartCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6025.SynchroniserPartCompoundDynamicAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2139.SynchroniserSleeve') -> 'Iterable[_6026.SynchroniserSleeveCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserSleeveCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6026.SynchroniserSleeveCompoundDynamicAnalysis))

    def results_for_torque_converter(self, design_entity: '_2140.TorqueConverter') -> 'Iterable[_6027.TorqueConverterCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6027.TorqueConverterCompoundDynamicAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2141.TorqueConverterPump') -> 'Iterable[_6029.TorqueConverterPumpCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterPumpCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6029.TorqueConverterPumpCompoundDynamicAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2143.TorqueConverterTurbine') -> 'Iterable[_6030.TorqueConverterTurbineCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterTurbineCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6030.TorqueConverterTurbineCompoundDynamicAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1837.CVTBeltConnection') -> 'Iterable[_5956.CVTBeltConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTBeltConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5956.CVTBeltConnectionCompoundDynamicAnalysis))

    def results_for_belt_connection(self, design_entity: '_1832.BeltConnection') -> 'Iterable[_5925.BeltConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BeltConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5925.BeltConnectionCompoundDynamicAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1833.CoaxialConnection') -> 'Iterable[_5940.CoaxialConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CoaxialConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5940.CoaxialConnectionCompoundDynamicAnalysis))

    def results_for_connection(self, design_entity: '_1836.Connection') -> 'Iterable[_5951.ConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5951.ConnectionCompoundDynamicAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1845.InterMountableComponentConnection') -> 'Iterable[_5977.InterMountableComponentConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.InterMountableComponentConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5977.InterMountableComponentConnectionCompoundDynamicAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1848.PlanetaryConnection') -> 'Iterable[_5995.PlanetaryConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetaryConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5995.PlanetaryConnectionCompoundDynamicAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1852.RollingRingConnection') -> 'Iterable[_6003.RollingRingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6003.RollingRingConnectionCompoundDynamicAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1856.ShaftToMountableComponentConnection') -> 'Iterable[_6007.ShaftToMountableComponentConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftToMountableComponentConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6007.ShaftToMountableComponentConnectionCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1862.BevelDifferentialGearMesh') -> 'Iterable[_5928.BevelDifferentialGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5928.BevelDifferentialGearMeshCompoundDynamicAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1866.ConceptGearMesh') -> 'Iterable[_5946.ConceptGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5946.ConceptGearMeshCompoundDynamicAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1872.FaceGearMesh') -> 'Iterable[_5966.FaceGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5966.FaceGearMeshCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1886.StraightBevelDiffGearMesh') -> 'Iterable[_6016.StraightBevelDiffGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6016.StraightBevelDiffGearMeshCompoundDynamicAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1864.BevelGearMesh') -> 'Iterable[_5933.BevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5933.BevelGearMeshCompoundDynamicAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1868.ConicalGearMesh') -> 'Iterable[_5949.ConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5949.ConicalGearMeshCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1860.AGMAGleasonConicalGearMesh') -> 'Iterable[_5921.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5921.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1870.CylindricalGearMesh') -> 'Iterable[_5960.CylindricalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5960.CylindricalGearMeshCompoundDynamicAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1876.HypoidGearMesh') -> 'Iterable[_5974.HypoidGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5974.HypoidGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_5979.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5979.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1880.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_5982.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5982.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1881.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_5985.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5985.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1884.SpiralBevelGearMesh') -> 'Iterable[_6010.SpiralBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6010.SpiralBevelGearMeshCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1888.StraightBevelGearMesh') -> 'Iterable[_6019.StraightBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6019.StraightBevelGearMeshCompoundDynamicAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1890.WormGearMesh') -> 'Iterable[_6034.WormGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6034.WormGearMeshCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1892.ZerolBevelGearMesh') -> 'Iterable[_6037.ZerolBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6037.ZerolBevelGearMeshCompoundDynamicAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1874.GearMesh') -> 'Iterable[_5970.GearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5970.GearMeshCompoundDynamicAnalysis))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1900.PartToPartShearCouplingConnection') -> 'Iterable[_5993.PartToPartShearCouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartToPartShearCouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5993.PartToPartShearCouplingConnectionCompoundDynamicAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1894.ClutchConnection') -> 'Iterable[_5938.ClutchConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5938.ClutchConnectionCompoundDynamicAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1896.ConceptCouplingConnection') -> 'Iterable[_5943.ConceptCouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5943.ConceptCouplingConnectionCompoundDynamicAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1898.CouplingConnection') -> 'Iterable[_5954.CouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5954.CouplingConnectionCompoundDynamicAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1902.SpringDamperConnection') -> 'Iterable[_6013.SpringDamperConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6013.SpringDamperConnectionCompoundDynamicAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1904.TorqueConverterConnection') -> 'Iterable[_6028.TorqueConverterConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6028.TorqueConverterConnectionCompoundDynamicAnalysis))
