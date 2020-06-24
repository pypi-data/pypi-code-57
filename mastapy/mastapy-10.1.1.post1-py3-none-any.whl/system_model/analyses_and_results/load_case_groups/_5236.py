'''_5236.py

ConceptSynchroGearEngagementStatus
'''


from mastapy.system_model.analyses_and_results.load_case_groups import _5239
from mastapy.system_model.part_model.gears import _2064
from mastapy._internal.python_net import python_net_import

_CONCEPT_SYNCHRO_GEAR_ENGAGEMENT_STATUS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'ConceptSynchroGearEngagementStatus')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptSynchroGearEngagementStatus',)


class ConceptSynchroGearEngagementStatus(_5239.GenericClutchEngagementStatus['_2064.CylindricalGear']):
    '''ConceptSynchroGearEngagementStatus

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_SYNCHRO_GEAR_ENGAGEMENT_STATUS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptSynchroGearEngagementStatus.TYPE'):
        super().__init__(instance_to_wrap)
