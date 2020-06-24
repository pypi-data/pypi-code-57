'''_187.py

ElementPropertiesRigid
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _211, _194
from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_RIGID = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ElementPropertiesRigid')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesRigid',)


class ElementPropertiesRigid(_194.ElementPropertiesBase):
    '''ElementPropertiesRigid

    This is a mastapy class.
    '''

    TYPE = _ELEMENT_PROPERTIES_RIGID
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElementPropertiesRigid.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_degree_of_freedom_inputs(self) -> 'int':
        '''int: 'NumberOfDegreeOfFreedomInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfDegreeOfFreedomInputs

    @property
    def degrees_of_freedom_list(self) -> 'List[_211.RigidElementNodeDegreesOfFreedom]':
        '''List[RigidElementNodeDegreesOfFreedom]: 'DegreesOfFreedomList' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.DegreesOfFreedomList, constructor.new(_211.RigidElementNodeDegreesOfFreedom))
        return value
