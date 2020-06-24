'''_3068.py

CylindricalGearMeshAdvancedSystemDeflection
'''


from typing import List, Callable

from mastapy.gears import _295
from mastapy._internal import constructor, conversion
from mastapy.scripting import _732
from mastapy.gears.gear_designs.cylindrical import _579, _583
from mastapy.gears.ltca.cylindrical import _875
from mastapy.math_utility import _897
from mastapy.system_model.connections_and_sockets.gears import _1798
from mastapy.system_model.analyses_and_results.static_loads import _2293
from mastapy.gears.rating.cylindrical import _475
from mastapy.system_model.analyses_and_results.system_deflections import _2180
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3118, _3077
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CylindricalGearMeshAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshAdvancedSystemDeflection',)


class CylindricalGearMeshAdvancedSystemDeflection(_3077.GearMeshAdvancedSystemDeflection):
    '''CylindricalGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def active_flank(self) -> '_295.CylindricalFlanks':
        '''CylindricalFlanks: 'ActiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ActiveFlank)
        return constructor.new(_295.CylindricalFlanks)(value) if value else None

    @property
    def inactive_flank(self) -> '_295.CylindricalFlanks':
        '''CylindricalFlanks: 'InactiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.InactiveFlank)
        return constructor.new(_295.CylindricalFlanks)(value) if value else None

    @property
    def peak_to_peak_te(self) -> 'float':
        '''float: 'PeakToPeakTE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PeakToPeakTE

    @property
    def mean_te_excluding_backlash(self) -> 'float':
        '''float: 'MeanTEExcludingBacklash' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanTEExcludingBacklash

    @property
    def torque_share(self) -> 'float':
        '''float: 'TorqueShare' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueShare

    @property
    def mean_mesh_tilt_stiffness(self) -> 'float':
        '''float: 'MeanMeshTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanMeshTiltStiffness

    @property
    def mean_mesh_stiffness(self) -> 'float':
        '''float: 'MeanMeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanMeshStiffness

    @property
    def peak_to_peak_mesh_stiffness(self) -> 'float':
        '''float: 'PeakToPeakMeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PeakToPeakMeshStiffness

    @property
    def mean_total_contact_ratio(self) -> 'float':
        '''float: 'MeanTotalContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanTotalContactRatio

    @property
    def maximum_contact_pressure(self) -> 'float':
        '''float: 'MaximumContactPressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumContactPressure

    @property
    def maximum_principal_root_stress_on_tension_side_from_gear_fe_model(self) -> 'List[float]':
        '''List[float]: 'MaximumPrincipalRootStressOnTensionSideFromGearFEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MaximumPrincipalRootStressOnTensionSideFromGearFEModel, float)
        return value

    @property
    def face_load_factor_contact(self) -> 'float':
        '''float: 'FaceLoadFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FaceLoadFactorContact

    @property
    def maximum_edge_stress(self) -> 'float':
        '''float: 'MaximumEdgeStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumEdgeStress

    @property
    def maximum_edge_stress_including_tip_contact(self) -> 'float':
        '''float: 'MaximumEdgeStressIncludingTipContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumEdgeStressIncludingTipContact

    @property
    def maximum_edge_stress_on_gear_a_including_tip_contact(self) -> 'float':
        '''float: 'MaximumEdgeStressOnGearAIncludingTipContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumEdgeStressOnGearAIncludingTipContact

    @property
    def maximum_edge_stress_on_gear_b_including_tip_contact(self) -> 'float':
        '''float: 'MaximumEdgeStressOnGearBIncludingTipContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumEdgeStressOnGearBIncludingTipContact

    @property
    def calculated_load_sharing_factor(self) -> 'float':
        '''float: 'CalculatedLoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculatedLoadSharingFactor

    @property
    def average_operating_transverse_contact_ratio_for_first_tooth_passing_period(self) -> 'float':
        '''float: 'AverageOperatingTransverseContactRatioForFirstToothPassingPeriod' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageOperatingTransverseContactRatioForFirstToothPassingPeriod

    @property
    def average_operating_axial_contact_ratio_for_first_tooth_passing_period(self) -> 'float':
        '''float: 'AverageOperatingAxialContactRatioForFirstToothPassingPeriod' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageOperatingAxialContactRatioForFirstToothPassingPeriod

    @property
    def use_advanced_ltca(self) -> 'bool':
        '''bool: 'UseAdvancedLTCA' is the original name of this property.'''

        return self.wrapped.UseAdvancedLTCA

    @use_advanced_ltca.setter
    def use_advanced_ltca(self, value: 'bool'):
        self.wrapped.UseAdvancedLTCA = bool(value) if value else False

    @property
    def contact_chart_max_pressure_gear_a(self) -> '_732.SMTBitmap':
        '''SMTBitmap: 'ContactChartMaxPressureGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_732.SMTBitmap)(self.wrapped.ContactChartMaxPressureGearA) if self.wrapped.ContactChartMaxPressureGearA else None

    @property
    def contact_chart_max_pressure_gear_a_as_text_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ContactChartMaxPressureGearAAsTextFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactChartMaxPressureGearAAsTextFile

    @property
    def contact_chart_max_pressure_gear_b(self) -> '_732.SMTBitmap':
        '''SMTBitmap: 'ContactChartMaxPressureGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_732.SMTBitmap)(self.wrapped.ContactChartMaxPressureGearB) if self.wrapped.ContactChartMaxPressureGearB else None

    @property
    def contact_chart_max_pressure_gear_b_as_text_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ContactChartMaxPressureGearBAsTextFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactChartMaxPressureGearBAsTextFile

    @property
    def contact_chart_gap_to_loaded_flank_gear_a(self) -> '_732.SMTBitmap':
        '''SMTBitmap: 'ContactChartGapToLoadedFlankGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_732.SMTBitmap)(self.wrapped.ContactChartGapToLoadedFlankGearA) if self.wrapped.ContactChartGapToLoadedFlankGearA else None

    @property
    def contact_chart_gap_to_loaded_flank_gear_a_as_text_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ContactChartGapToLoadedFlankGearAAsTextFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactChartGapToLoadedFlankGearAAsTextFile

    @property
    def contact_chart_gap_to_loaded_flank_gear_b(self) -> '_732.SMTBitmap':
        '''SMTBitmap: 'ContactChartGapToLoadedFlankGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_732.SMTBitmap)(self.wrapped.ContactChartGapToLoadedFlankGearB) if self.wrapped.ContactChartGapToLoadedFlankGearB else None

    @property
    def contact_chart_gap_to_loaded_flank_gear_b_as_text_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ContactChartGapToLoadedFlankGearBAsTextFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactChartGapToLoadedFlankGearBAsTextFile

    @property
    def contact_chart_gap_to_unloaded_flank_gear_a(self) -> '_732.SMTBitmap':
        '''SMTBitmap: 'ContactChartGapToUnloadedFlankGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_732.SMTBitmap)(self.wrapped.ContactChartGapToUnloadedFlankGearA) if self.wrapped.ContactChartGapToUnloadedFlankGearA else None

    @property
    def contact_chart_gap_to_unloaded_flank_gear_a_as_text_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ContactChartGapToUnloadedFlankGearAAsTextFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactChartGapToUnloadedFlankGearAAsTextFile

    @property
    def contact_chart_gap_to_unloaded_flank_gear_b(self) -> '_732.SMTBitmap':
        '''SMTBitmap: 'ContactChartGapToUnloadedFlankGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_732.SMTBitmap)(self.wrapped.ContactChartGapToUnloadedFlankGearB) if self.wrapped.ContactChartGapToUnloadedFlankGearB else None

    @property
    def contact_chart_gap_to_unloaded_flank_gear_b_as_text_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ContactChartGapToUnloadedFlankGearBAsTextFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactChartGapToUnloadedFlankGearBAsTextFile

    @property
    def gear_mesh_design(self) -> '_579.CylindricalGearMeshDesign':
        '''CylindricalGearMeshDesign: 'GearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_579.CylindricalGearMeshDesign)(self.wrapped.GearMeshDesign) if self.wrapped.GearMeshDesign else None

    @property
    def point_with_maximum_contact_pressure(self) -> '_875.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'PointWithMaximumContactPressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_875.CylindricalGearMeshLoadedContactPoint)(self.wrapped.PointWithMaximumContactPressure) if self.wrapped.PointWithMaximumContactPressure else None

    @property
    def transmission_error_fourier_series_for_first_tooth_passing_period(self) -> '_897.FourierSeries':
        '''FourierSeries: 'TransmissionErrorFourierSeriesForFirstToothPassingPeriod' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.FourierSeries)(self.wrapped.TransmissionErrorFourierSeriesForFirstToothPassingPeriod) if self.wrapped.TransmissionErrorFourierSeriesForFirstToothPassingPeriod else None

    @property
    def connection_design(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_2293.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2293.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_475.CylindricalGearMeshRating':
        '''CylindricalGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_475.CylindricalGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def cylindrical_gear_mesh_system_deflection_results(self) -> 'List[_2180.CylindricalGearMeshSystemDeflectionTimestep]':
        '''List[CylindricalGearMeshSystemDeflectionTimestep]: 'CylindricalGearMeshSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearMeshSystemDeflectionResults, constructor.new(_2180.CylindricalGearMeshSystemDeflectionTimestep))
        return value

    @property
    def gear_designs(self) -> 'List[_583.CylindricalGearDesign]':
        '''List[CylindricalGearDesign]: 'GearDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearDesigns, constructor.new(_583.CylindricalGearDesign))
        return value

    @property
    def cylindrical_gear_advanced_analyses(self) -> 'List[_3118.CylindricalGearAdvancedSystemDeflection]':
        '''List[CylindricalGearAdvancedSystemDeflection]: 'CylindricalGearAdvancedAnalyses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearAdvancedAnalyses, constructor.new(_3118.CylindricalGearAdvancedSystemDeflection))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshAdvancedSystemDeflection]':
        '''List[CylindricalGearMeshAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshAdvancedSystemDeflection))
        return value
