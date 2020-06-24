'''_4132.py

ShaftHubConnectionPowerFlow
'''


from mastapy.system_model.part_model.couplings import _1967
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2188
from mastapy.detailed_rigid_connectors.rating import _1174
from mastapy.detailed_rigid_connectors.interference_fits.rating import _1187
from mastapy._internal.cast_exception import CastException
from mastapy.detailed_rigid_connectors.splines.ratings import (
    _1162, _1164, _1166, _1168
)
from mastapy.detailed_rigid_connectors.keyed_joints.rating import _1180
from mastapy.system_model.analyses_and_results.power_flows import _4180
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ShaftHubConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionPowerFlow',)


class ShaftHubConnectionPowerFlow(_4180.ConnectorPowerFlow):
    '''ShaftHubConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1967.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1967.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2188.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2188.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_1174.ShaftHubConnectionRating':
        '''ShaftHubConnectionRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1174.ShaftHubConnectionRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_interference_fit_rating(self) -> '_1187.InterferenceFitRating':
        '''InterferenceFitRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__ != 'InterferenceFitRating':
            raise CastException('Failed to cast component_detailed_analysis to InterferenceFitRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1187.InterferenceFitRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_agma6123_spline_joint_rating(self) -> '_1162.AGMA6123SplineJointRating':
        '''AGMA6123SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__ != 'AGMA6123SplineJointRating':
            raise CastException('Failed to cast component_detailed_analysis to AGMA6123SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1162.AGMA6123SplineJointRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_din5466_spline_rating(self) -> '_1164.DIN5466SplineRating':
        '''DIN5466SplineRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__ != 'DIN5466SplineRating':
            raise CastException('Failed to cast component_detailed_analysis to DIN5466SplineRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1164.DIN5466SplineRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_gbt17855_spline_joint_rating(self) -> '_1166.GBT17855SplineJointRating':
        '''GBT17855SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__ != 'GBT17855SplineJointRating':
            raise CastException('Failed to cast component_detailed_analysis to GBT17855SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1166.GBT17855SplineJointRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_sae_spline_joint_rating(self) -> '_1168.SAESplineJointRating':
        '''SAESplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__ != 'SAESplineJointRating':
            raise CastException('Failed to cast component_detailed_analysis to SAESplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1168.SAESplineJointRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_keyway_rating(self) -> '_1180.KeywayRating':
        '''KeywayRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__ != 'KeywayRating':
            raise CastException('Failed to cast component_detailed_analysis to KeywayRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1180.KeywayRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
