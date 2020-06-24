'''_6227.py

GearWhineAnalysisResultsBrokenDownByGroupsWithinAHarmonic
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.reportable_property_results import _6228
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_WHINE_ANALYSIS_RESULTS_BROKEN_DOWN_BY_GROUPS_WITHIN_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.ReportablePropertyResults', 'GearWhineAnalysisResultsBrokenDownByGroupsWithinAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('GearWhineAnalysisResultsBrokenDownByGroupsWithinAHarmonic',)


class GearWhineAnalysisResultsBrokenDownByGroupsWithinAHarmonic(_1.APIBase):
    '''GearWhineAnalysisResultsBrokenDownByGroupsWithinAHarmonic

    This is a mastapy class.
    '''

    TYPE = _GEAR_WHINE_ANALYSIS_RESULTS_BROKEN_DOWN_BY_GROUPS_WITHIN_A_HARMONIC
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearWhineAnalysisResultsBrokenDownByGroupsWithinAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def locations_global_coordinate_system(self) -> 'List[_6228.GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic]':
        '''List[GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic]: 'LocationsGlobalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LocationsGlobalCoordinateSystem, constructor.new(_6228.GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic))
        return value

    @property
    def locations_local_coordinate_system(self) -> 'List[_6228.GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic]':
        '''List[GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic]: 'LocationsLocalCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LocationsLocalCoordinateSystem, constructor.new(_6228.GearWhineAnalysisResultsBrokenDownByLocationWithinAHarmonic))
        return value
