'''_1126.py

DetailedRigidConnectorHalfDesign
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DETAILED_RIGID_CONNECTOR_HALF_DESIGN = python_net_import('SMT.MastaAPI.DetailedRigidConnectors', 'DetailedRigidConnectorHalfDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('DetailedRigidConnectorHalfDesign',)


class DetailedRigidConnectorHalfDesign(_1.APIBase):
    '''DetailedRigidConnectorHalfDesign

    This is a mastapy class.
    '''

    TYPE = _DETAILED_RIGID_CONNECTOR_HALF_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DetailedRigidConnectorHalfDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def non_contacting_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NonContactingDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NonContactingDiameter) if self.wrapped.NonContactingDiameter else None

    @non_contacting_diameter.setter
    def non_contacting_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.NonContactingDiameter = value

    @property
    def tensile_yield_strength(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'TensileYieldStrength' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.TensileYieldStrength) if self.wrapped.TensileYieldStrength else None

    @tensile_yield_strength.setter
    def tensile_yield_strength(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.TensileYieldStrength = value

    @property
    def ultimate_tensile_strength(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'UltimateTensileStrength' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.UltimateTensileStrength) if self.wrapped.UltimateTensileStrength else None

    @ultimate_tensile_strength.setter
    def ultimate_tensile_strength(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.UltimateTensileStrength = value
