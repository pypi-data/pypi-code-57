'''_1753.py

ConcentricPartGroupCombinationSystemDeflectionShaftResults
'''


from typing import List

from mastapy.system_model.analyses_and_results.system_deflections import _2066
from mastapy._internal import constructor, conversion
from mastapy.system_model.drawing import _1757
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CONCENTRIC_PART_GROUP_COMBINATION_SYSTEM_DEFLECTION_SHAFT_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.Drawing', 'ConcentricPartGroupCombinationSystemDeflectionShaftResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ConcentricPartGroupCombinationSystemDeflectionShaftResults',)


class ConcentricPartGroupCombinationSystemDeflectionShaftResults(_1.APIBase):
    '''ConcentricPartGroupCombinationSystemDeflectionShaftResults

    This is a mastapy class.
    '''

    TYPE = _CONCENTRIC_PART_GROUP_COMBINATION_SYSTEM_DEFLECTION_SHAFT_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConcentricPartGroupCombinationSystemDeflectionShaftResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def shaft_system_deflection(self) -> '_2066.ShaftSystemDeflection':
        '''ShaftSystemDeflection: 'ShaftSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2066.ShaftSystemDeflection)(self.wrapped.ShaftSystemDeflection) if self.wrapped.ShaftSystemDeflection else None

    @property
    def node_results(self) -> 'List[_1757.ShaftDeflectionDrawingNodeItem]':
        '''List[ShaftDeflectionDrawingNodeItem]: 'NodeResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.NodeResults, constructor.new(_1757.ShaftDeflectionDrawingNodeItem))
        return value
