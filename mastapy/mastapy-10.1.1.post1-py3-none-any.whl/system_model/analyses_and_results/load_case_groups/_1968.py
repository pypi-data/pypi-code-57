'''_1968.py

DesignState
'''


from typing import List, Optional

from mastapy.system_model.analyses_and_results.load_case_groups import _6168, _6169, _6167
from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets.couplings import _1822
from mastapy.system_model.part_model.gears import _2005
from mastapy.system_model.analyses_and_results.static_loads import _1969
from mastapy._internal.python_net import python_net_import

_DESIGN_STATE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'DesignState')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignState',)


class DesignState(_6167.AbstractDesignStateLoadCaseGroup):
    '''DesignState

    This is a mastapy class.
    '''

    TYPE = _DESIGN_STATE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignState.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def clutches(self) -> 'List[_6168.ClutchEngagementStatus]':
        '''List[ClutchEngagementStatus]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6168.ClutchEngagementStatus))
        return value

    @property
    def concept_synchro_mounted_gears(self) -> 'List[_6169.ConceptSynchroGearEngagementStatus]':
        '''List[ConceptSynchroGearEngagementStatus]: 'ConceptSynchroMountedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptSynchroMountedGears, constructor.new(_6169.ConceptSynchroGearEngagementStatus))
        return value

    def clutch_engagement_status_for(self, clutch_connection: '_1822.ClutchConnection') -> '_6168.ClutchEngagementStatus':
        ''' 'ClutchEngagementStatusFor' is the original name of this method.

        Args:
            clutch_connection (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.load_case_groups.ClutchEngagementStatus
        '''

        method_result = self.wrapped.ClutchEngagementStatusFor(clutch_connection.wrapped if clutch_connection else None)
        return constructor.new(_6168.ClutchEngagementStatus)(method_result) if method_result else None

    def concept_synchro_gear_engagement_status_for(self, gear: '_2005.CylindricalGear') -> '_6169.ConceptSynchroGearEngagementStatus':
        ''' 'ConceptSynchroGearEngagementStatusFor' is the original name of this method.

        Args:
            gear (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.load_case_groups.ConceptSynchroGearEngagementStatus
        '''

        method_result = self.wrapped.ConceptSynchroGearEngagementStatusFor(gear.wrapped if gear else None)
        return constructor.new(_6169.ConceptSynchroGearEngagementStatus)(method_result) if method_result else None

    def create_load_case(self, name: Optional['str'] = 'New Static Load') -> '_1969.StaticLoadCase':
        ''' 'CreateLoadCase' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase
        '''

        name = str(name)
        method_result = self.wrapped.CreateLoadCase(name if name else None)
        return constructor.new(_1969.StaticLoadCase)(method_result) if method_result else None

    def delete(self):
        ''' 'Delete' is the original name of this method.'''

        self.wrapped.Delete()
