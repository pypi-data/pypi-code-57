'''_6177.py

DesignEntityStaticLoadCaseGroup
'''


from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DESIGN_ENTITY_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups', 'DesignEntityStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignEntityStaticLoadCaseGroup',)


class DesignEntityStaticLoadCaseGroup(_1.APIBase):
    '''DesignEntityStaticLoadCaseGroup

    This is a mastapy class.
    '''

    TYPE = _DESIGN_ENTITY_STATIC_LOAD_CASE_GROUP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignEntityStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)
