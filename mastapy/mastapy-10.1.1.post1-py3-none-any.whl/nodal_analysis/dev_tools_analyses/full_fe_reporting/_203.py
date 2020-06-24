'''_203.py

ElementPropertiesMass
'''


from mastapy._internal.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy.math_utility import _219
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _200
from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_MASS = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ElementPropertiesMass')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesMass',)


class ElementPropertiesMass(_200.ElementPropertiesBase):
    '''ElementPropertiesMass

    This is a mastapy class.
    '''

    TYPE = _ELEMENT_PROPERTIES_MASS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElementPropertiesMass.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def mass(self) -> 'Vector3D':
        '''Vector3D: 'Mass' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_vector3d(self.wrapped.Mass)
        return value

    @property
    def inertia(self) -> '_219.InertiaTensor':
        '''InertiaTensor: 'Inertia' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_219.InertiaTensor)(self.wrapped.Inertia) if self.wrapped.Inertia else None
