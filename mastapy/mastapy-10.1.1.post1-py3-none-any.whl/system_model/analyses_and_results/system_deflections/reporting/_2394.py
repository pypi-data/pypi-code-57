'''_2394.py

RigidlyConnectedComponentGroupSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2158
from mastapy.system_model.analyses_and_results import _2110
from mastapy._internal.python_net import python_net_import

_RIGIDLY_CONNECTED_COMPONENT_GROUP_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting', 'RigidlyConnectedComponentGroupSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RigidlyConnectedComponentGroupSystemDeflection',)


class RigidlyConnectedComponentGroupSystemDeflection(_2110.DesignEntityGroupAnalysis):
    '''RigidlyConnectedComponentGroupSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _RIGIDLY_CONNECTED_COMPONENT_GROUP_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RigidlyConnectedComponentGroupSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def mass(self) -> 'float':
        '''float: 'Mass' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Mass

    @property
    def polar_inertia(self) -> 'float':
        '''float: 'PolarInertia' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PolarInertia

    @property
    def components(self) -> 'List[_2158.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'Components' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Components, constructor.new(_2158.ComponentSystemDeflection))
        return value
