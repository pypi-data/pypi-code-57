'''_817.py

FlankMeasurementBorder
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FLANK_MEASUREMENT_BORDER = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'FlankMeasurementBorder')


__docformat__ = 'restructuredtext en'
__all__ = ('FlankMeasurementBorder',)


class FlankMeasurementBorder(_1.APIBase):
    '''FlankMeasurementBorder

    This is a mastapy class.
    '''

    TYPE = _FLANK_MEASUREMENT_BORDER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlankMeasurementBorder.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def percent_of_face_width_at_heel(self) -> 'float':
        '''float: 'PercentOfFaceWidthAtHeel' is the original name of this property.'''

        return self.wrapped.PercentOfFaceWidthAtHeel

    @percent_of_face_width_at_heel.setter
    def percent_of_face_width_at_heel(self, value: 'float'):
        self.wrapped.PercentOfFaceWidthAtHeel = float(value) if value else 0.0

    @property
    def percent_of_face_width_at_toe(self) -> 'float':
        '''float: 'PercentOfFaceWidthAtToe' is the original name of this property.'''

        return self.wrapped.PercentOfFaceWidthAtToe

    @percent_of_face_width_at_toe.setter
    def percent_of_face_width_at_toe(self, value: 'float'):
        self.wrapped.PercentOfFaceWidthAtToe = float(value) if value else 0.0

    @property
    def percent_of_working_depth_at_tip(self) -> 'float':
        '''float: 'PercentOfWorkingDepthAtTip' is the original name of this property.'''

        return self.wrapped.PercentOfWorkingDepthAtTip

    @percent_of_working_depth_at_tip.setter
    def percent_of_working_depth_at_tip(self, value: 'float'):
        self.wrapped.PercentOfWorkingDepthAtTip = float(value) if value else 0.0

    @property
    def percent_of_working_depth_at_root(self) -> 'float':
        '''float: 'PercentOfWorkingDepthAtRoot' is the original name of this property.'''

        return self.wrapped.PercentOfWorkingDepthAtRoot

    @percent_of_working_depth_at_root.setter
    def percent_of_working_depth_at_root(self, value: 'float'):
        self.wrapped.PercentOfWorkingDepthAtRoot = float(value) if value else 0.0
