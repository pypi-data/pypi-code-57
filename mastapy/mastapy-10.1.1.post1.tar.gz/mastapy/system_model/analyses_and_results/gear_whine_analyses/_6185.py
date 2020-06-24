'''_6185.py

SpeedOptionsForGearWhineAnalysisResults
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy.system_model.analyses_and_results.analysis_cases import _3380
from mastapy.system_model.analyses_and_results.static_loads import _2057
from mastapy._internal.python_net import python_net_import

_SPEED_OPTIONS_FOR_GEAR_WHINE_ANALYSIS_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'SpeedOptionsForGearWhineAnalysisResults')


__docformat__ = 'restructuredtext en'
__all__ = ('SpeedOptionsForGearWhineAnalysisResults',)


class SpeedOptionsForGearWhineAnalysisResults(_3380.AbstractAnalysisOptions['_2057.StaticLoadCase']):
    '''SpeedOptionsForGearWhineAnalysisResults

    This is a mastapy class.
    '''

    TYPE = _SPEED_OPTIONS_FOR_GEAR_WHINE_ANALYSIS_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpeedOptionsForGearWhineAnalysisResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def minimum(self) -> 'float':
        '''float: 'Minimum' is the original name of this property.'''

        return self.wrapped.Minimum

    @minimum.setter
    def minimum(self, value: 'float'):
        self.wrapped.Minimum = float(value) if value else 0.0

    @property
    def maximum(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'Maximum' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.Maximum) if self.wrapped.Maximum else None

    @maximum.setter
    def maximum(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.Maximum = value

    @property
    def reference_power_load_speed(self) -> 'float':
        '''float: 'ReferencePowerLoadSpeed' is the original name of this property.'''

        return self.wrapped.ReferencePowerLoadSpeed

    @reference_power_load_speed.setter
    def reference_power_load_speed(self, value: 'float'):
        self.wrapped.ReferencePowerLoadSpeed = float(value) if value else 0.0
