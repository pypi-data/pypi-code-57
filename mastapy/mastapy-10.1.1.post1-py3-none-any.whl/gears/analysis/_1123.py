'''_1123.py

GearSetGroupDutyCycle
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating import _340
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_SET_GROUP_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearSetGroupDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetGroupDutyCycle',)


class GearSetGroupDutyCycle(_1.APIBase):
    '''GearSetGroupDutyCycle

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_GROUP_DUTY_CYCLE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetGroupDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def analysis_name(self) -> 'str':
        '''str: 'AnalysisName' is the original name of this property.'''

        return self.wrapped.AnalysisName

    @analysis_name.setter
    def analysis_name(self, value: 'str'):
        self.wrapped.AnalysisName = str(value) if value else None

    @property
    def total_duration(self) -> 'float':
        '''float: 'TotalDuration' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalDuration

    @property
    def normalized_safety_factor_for_fatigue_and_static(self) -> 'float':
        '''float: 'NormalizedSafetyFactorForFatigueAndStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedSafetyFactorForFatigueAndStatic

    @property
    def normalized_safety_factor_for_fatigue(self) -> 'float':
        '''float: 'NormalizedSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedSafetyFactorForFatigue

    @property
    def normalized_safety_factor_for_static(self) -> 'float':
        '''float: 'NormalizedSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedSafetyFactorForStatic

    @property
    def normalized_bending_safety_factor_for_fatigue(self) -> 'float':
        '''float: 'NormalizedBendingSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedBendingSafetyFactorForFatigue

    @property
    def normalized_bending_safety_factor_for_static(self) -> 'float':
        '''float: 'NormalizedBendingSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedBendingSafetyFactorForStatic

    @property
    def normalized_contact_safety_factor_for_fatigue(self) -> 'float':
        '''float: 'NormalizedContactSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedContactSafetyFactorForFatigue

    @property
    def normalized_contact_safety_factor_for_static(self) -> 'float':
        '''float: 'NormalizedContactSafetyFactorForStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalizedContactSafetyFactorForStatic

    @property
    def loaded_rating_duty_cycles(self) -> 'List[_340.GearSetDutyCycleRating]':
        '''List[GearSetDutyCycleRating]: 'LoadedRatingDutyCycles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadedRatingDutyCycles, constructor.new(_340.GearSetDutyCycleRating))
        return value

    @property
    def rating_duty_cycles(self) -> 'List[_340.GearSetDutyCycleRating]':
        '''List[GearSetDutyCycleRating]: 'RatingDutyCycles' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RatingDutyCycles, constructor.new(_340.GearSetDutyCycleRating))
        return value
