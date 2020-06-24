'''_720.py

CutterSimulationCalc
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _681, _731
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _768
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CUTTER_SIMULATION_CALC = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'CutterSimulationCalc')


__docformat__ = 'restructuredtext en'
__all__ = ('CutterSimulationCalc',)


class CutterSimulationCalc(_1.APIBase):
    '''CutterSimulationCalc

    This is a mastapy class.
    '''

    TYPE = _CUTTER_SIMULATION_CALC
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CutterSimulationCalc.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def normal_tooth_thickness_on_the_v_circle(self) -> 'float':
        '''float: 'NormalToothThicknessOnTheVCircle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalToothThicknessOnTheVCircle

    @property
    def normal_tooth_thickness_on_the_reference_circle(self) -> 'float':
        '''float: 'NormalToothThicknessOnTheReferenceCircle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalToothThicknessOnTheReferenceCircle

    @property
    def normal_thickness_at_tip_form_diameter(self) -> 'float':
        '''float: 'NormalThicknessAtTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalThicknessAtTipFormDiameter

    @property
    def normal_tip_thickness(self) -> 'float':
        '''float: 'NormalTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalTipThickness

    @property
    def profile_shift_coefficient(self) -> 'float':
        '''float: 'ProfileShiftCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ProfileShiftCoefficient

    @property
    def tip_form_diameter(self) -> 'float':
        '''float: 'TipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TipFormDiameter

    @property
    def tip_diameter(self) -> 'float':
        '''float: 'TipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TipDiameter

    @property
    def root_diameter(self) -> 'float':
        '''float: 'RootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RootDiameter

    @property
    def root_form_diameter(self) -> 'float':
        '''float: 'RootFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RootFormDiameter

    @property
    def rough_root_form_diameter(self) -> 'float':
        '''float: 'RoughRootFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RoughRootFormDiameter

    @property
    def chamfer_transverse_pressure_angle_at_tip_form_diameter(self) -> 'float':
        '''float: 'ChamferTransversePressureAngleAtTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ChamferTransversePressureAngleAtTipFormDiameter

    @property
    def transverse_chamfer_angle_tangent_to_involute_at_tip_form_diameter(self) -> 'float':
        '''float: 'TransverseChamferAngleTangentToInvoluteAtTipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseChamferAngleTangentToInvoluteAtTipFormDiameter

    @property
    def residual_fillet_undercut(self) -> 'float':
        '''float: 'ResidualFilletUndercut' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ResidualFilletUndercut

    @property
    def residual_fillet_undercut_diameter(self) -> 'float':
        '''float: 'ResidualFilletUndercutDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ResidualFilletUndercutDiameter

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def transverse_chamfer_angle_straight_line_approximation(self) -> 'float':
        '''float: 'TransverseChamferAngleStraightLineApproximation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseChamferAngleStraightLineApproximation

    @property
    def sap_to_form_radius_clearance(self) -> 'float':
        '''float: 'SAPToFormRadiusClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SAPToFormRadiusClearance

    @property
    def base_to_form_radius_clearance(self) -> 'float':
        '''float: 'BaseToFormRadiusClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BaseToFormRadiusClearance

    @property
    def normal_thickness_at_form_diameter(self) -> 'float':
        '''float: 'NormalThicknessAtFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalThicknessAtFormDiameter

    @property
    def reference_diameter(self) -> 'float':
        '''float: 'ReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReferenceDiameter

    @property
    def base_diameter(self) -> 'float':
        '''float: 'BaseDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BaseDiameter

    @property
    def lowest_sap_diameter(self) -> 'float':
        '''float: 'LowestSAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LowestSAPDiameter

    @property
    def maximum_finish_stock_arc_length(self) -> 'float':
        '''float: 'MaximumFinishStockArcLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumFinishStockArcLength

    @property
    def minimum_finish_stock_arc_length(self) -> 'float':
        '''float: 'MinimumFinishStockArcLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumFinishStockArcLength

    @property
    def finish_cutter_tip_to_fillet_clearance(self) -> 'float':
        '''float: 'FinishCutterTipToFilletClearance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FinishCutterTipToFilletClearance

    @property
    def theoretical_finish_root_form_diameter(self) -> 'float':
        '''float: 'TheoreticalFinishRootFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TheoreticalFinishRootFormDiameter

    @property
    def transverse_root_fillet_radius(self) -> 'float':
        '''float: 'TransverseRootFilletRadius' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseRootFilletRadius

    @property
    def generating_circle_diameter(self) -> 'float':
        '''float: 'GeneratingCircleDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.GeneratingCircleDiameter

    @property
    def gear(self) -> '_681.CylindricalCutterSimulatableGear':
        '''CylindricalCutterSimulatableGear: 'Gear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_681.CylindricalCutterSimulatableGear)(self.wrapped.Gear) if self.wrapped.Gear else None

    @property
    def stock_removed_at_reference_diameter(self) -> '_731.FinishStockPoint':
        '''FinishStockPoint: 'StockRemovedAtReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_731.FinishStockPoint)(self.wrapped.StockRemovedAtReferenceDiameter) if self.wrapped.StockRemovedAtReferenceDiameter else None

    @property
    def stock_removed_at_designed_sap(self) -> '_731.FinishStockPoint':
        '''FinishStockPoint: 'StockRemovedAtDesignedSAP' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_731.FinishStockPoint)(self.wrapped.StockRemovedAtDesignedSAP) if self.wrapped.StockRemovedAtDesignedSAP else None

    @property
    def stock_removed_at_rough_tip_form(self) -> '_731.FinishStockPoint':
        '''FinishStockPoint: 'StockRemovedAtRoughTipForm' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_731.FinishStockPoint)(self.wrapped.StockRemovedAtRoughTipForm) if self.wrapped.StockRemovedAtRoughTipForm else None

    @property
    def gear_fillet_points(self) -> 'List[_768.NamedPoint]':
        '''List[NamedPoint]: 'GearFilletPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearFilletPoints, constructor.new(_768.NamedPoint))
        return value

    @property
    def finish_stock_indexed_arcs(self) -> 'List[_731.FinishStockPoint]':
        '''List[FinishStockPoint]: 'FinishStockIndexedArcs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FinishStockIndexedArcs, constructor.new(_731.FinishStockPoint))
        return value

    @property
    def main_profile_finish_stock(self) -> 'List[_731.FinishStockPoint]':
        '''List[FinishStockPoint]: 'MainProfileFinishStock' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MainProfileFinishStock, constructor.new(_731.FinishStockPoint))
        return value
