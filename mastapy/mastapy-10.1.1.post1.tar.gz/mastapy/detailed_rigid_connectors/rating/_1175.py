'''_1175.py

ShaftHubConnectionRating
'''


from mastapy._internal import constructor
from mastapy.detailed_rigid_connectors import _1126
from mastapy.detailed_rigid_connectors.interference_fits import _1184
from mastapy._internal.cast_exception import CastException
from mastapy.detailed_rigid_connectors.splines import (
    _1129, _1132, _1139, _1147,
    _1136, _1140
)
from mastapy.detailed_rigid_connectors.keyed_joints import _1176
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_RATING = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Rating', 'ShaftHubConnectionRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionRating',)


class ShaftHubConnectionRating(_1.APIBase):
    '''ShaftHubConnectionRating

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_RATING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def additional_rating_information(self) -> 'str':
        '''str: 'AdditionalRatingInformation' is the original name of this property.'''

        return self.wrapped.AdditionalRatingInformation

    @additional_rating_information.setter
    def additional_rating_information(self, value: 'str'):
        self.wrapped.AdditionalRatingInformation = str(value) if value else None

    @property
    def joint_design(self) -> '_1126.DetailedRigidConnectorDesign':
        '''DetailedRigidConnectorDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1126.DetailedRigidConnectorDesign)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_interference_fit_design(self) -> '_1184.InterferenceFitDesign':
        '''InterferenceFitDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.JointDesign.__class__.__qualname__ != 'InterferenceFitDesign':
            raise CastException('Failed to cast joint_design to InterferenceFitDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new(_1184.InterferenceFitDesign)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_custom_spline_joint_design(self) -> '_1129.CustomSplineJointDesign':
        '''CustomSplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.JointDesign.__class__.__qualname__ != 'CustomSplineJointDesign':
            raise CastException('Failed to cast joint_design to CustomSplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new(_1129.CustomSplineJointDesign)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_din5480_spline_joint_design(self) -> '_1132.DIN5480SplineJointDesign':
        '''DIN5480SplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.JointDesign.__class__.__qualname__ != 'DIN5480SplineJointDesign':
            raise CastException('Failed to cast joint_design to DIN5480SplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new(_1132.DIN5480SplineJointDesign)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_iso4156_spline_joint_design(self) -> '_1139.ISO4156SplineJointDesign':
        '''ISO4156SplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.JointDesign.__class__.__qualname__ != 'ISO4156SplineJointDesign':
            raise CastException('Failed to cast joint_design to ISO4156SplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new(_1139.ISO4156SplineJointDesign)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_sae_spline_joint_design(self) -> '_1147.SAESplineJointDesign':
        '''SAESplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.JointDesign.__class__.__qualname__ != 'SAESplineJointDesign':
            raise CastException('Failed to cast joint_design to SAESplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new(_1147.SAESplineJointDesign)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_gbt3478_spline_joint_design(self) -> '_1136.GBT3478SplineJointDesign':
        '''GBT3478SplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.JointDesign.__class__.__qualname__ != 'GBT3478SplineJointDesign':
            raise CastException('Failed to cast joint_design to GBT3478SplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new(_1136.GBT3478SplineJointDesign)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_jisb1603_spline_joint_design(self) -> '_1140.JISB1603SplineJointDesign':
        '''JISB1603SplineJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.JointDesign.__class__.__qualname__ != 'JISB1603SplineJointDesign':
            raise CastException('Failed to cast joint_design to JISB1603SplineJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new(_1140.JISB1603SplineJointDesign)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None

    @property
    def joint_design_of_type_keyed_joint_design(self) -> '_1176.KeyedJointDesign':
        '''KeyedJointDesign: 'JointDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.JointDesign.__class__.__qualname__ != 'KeyedJointDesign':
            raise CastException('Failed to cast joint_design to KeyedJointDesign. Expected: {}.'.format(self.wrapped.JointDesign.__class__.__qualname__))

        return constructor.new(_1176.KeyedJointDesign)(self.wrapped.JointDesign) if self.wrapped.JointDesign else None
