'''_346.py

FaceMeshLoadCase
'''


from mastapy.gears import _296
from mastapy._internal import constructor, conversion
from mastapy.gears.load_case import _344
from mastapy._internal.python_net import python_net_import

_FACE_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.Gears.LoadCase.Face', 'FaceMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceMeshLoadCase',)


class FaceMeshLoadCase(_344.MeshLoadCase):
    '''FaceMeshLoadCase

    This is a mastapy class.
    '''

    TYPE = _FACE_MESH_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def misalignment_source(self) -> '_296.CylindricalMisalignmentDataSource':
        '''CylindricalMisalignmentDataSource: 'MisalignmentSource' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.MisalignmentSource)
        return constructor.new(_296.CylindricalMisalignmentDataSource)(value) if value else None

    @misalignment_source.setter
    def misalignment_source(self, value: '_296.CylindricalMisalignmentDataSource'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MisalignmentSource = value

    @property
    def equivalent_misalignment_due_to_system_deflection(self) -> 'float':
        '''float: 'EquivalentMisalignmentDueToSystemDeflection' is the original name of this property.'''

        return self.wrapped.EquivalentMisalignmentDueToSystemDeflection

    @equivalent_misalignment_due_to_system_deflection.setter
    def equivalent_misalignment_due_to_system_deflection(self, value: 'float'):
        self.wrapped.EquivalentMisalignmentDueToSystemDeflection = float(value) if value else 0.0
