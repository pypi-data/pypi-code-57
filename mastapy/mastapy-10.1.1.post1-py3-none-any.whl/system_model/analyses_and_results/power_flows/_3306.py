'''_3306.py

ShaftHubConnectionPowerFlow
'''


from mastapy.system_model.part_model.couplings import _2132
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6173
from mastapy.detailed_rigid_connectors.rating import _1019
from mastapy.detailed_rigid_connectors.splines.ratings import (
    _1007, _1009, _1011, _1013,
    _1015
)
from mastapy._internal.cast_exception import CastException
from mastapy.detailed_rigid_connectors.keyed_joints.rating import _1025
from mastapy.detailed_rigid_connectors.interference_fits.rating import _1032
from mastapy.system_model.analyses_and_results.power_flows import _3250
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ShaftHubConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionPowerFlow',)


class ShaftHubConnectionPowerFlow(_3250.ConnectorPowerFlow):
    '''ShaftHubConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2132.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6173.ShaftHubConnectionLoadCase':
        '''ShaftHubConnectionLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6173.ShaftHubConnectionLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_1019.ShaftHubConnectionRating':
        '''ShaftHubConnectionRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1019.ShaftHubConnectionRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_agma6123_spline_joint_rating(self) -> '_1007.AGMA6123SplineJointRating':
        '''AGMA6123SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1007.AGMA6123SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to AGMA6123SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1007.AGMA6123SplineJointRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_din5466_spline_rating(self) -> '_1009.DIN5466SplineRating':
        '''DIN5466SplineRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1009.DIN5466SplineRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to DIN5466SplineRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1009.DIN5466SplineRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_gbt17855_spline_joint_rating(self) -> '_1011.GBT17855SplineJointRating':
        '''GBT17855SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1011.GBT17855SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to GBT17855SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1011.GBT17855SplineJointRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_sae_spline_joint_rating(self) -> '_1013.SAESplineJointRating':
        '''SAESplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1013.SAESplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SAESplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1013.SAESplineJointRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_spline_joint_rating(self) -> '_1015.SplineJointRating':
        '''SplineJointRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1015.SplineJointRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to SplineJointRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1015.SplineJointRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_keyway_rating(self) -> '_1025.KeywayRating':
        '''KeywayRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1025.KeywayRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to KeywayRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1025.KeywayRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_interference_fit_rating(self) -> '_1032.InterferenceFitRating':
        '''InterferenceFitRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1032.InterferenceFitRating.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to InterferenceFitRating. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new(_1032.InterferenceFitRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
