'''_6056.py

BeltDriveLoadCase
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2111
from mastapy.system_model.analyses_and_results.static_loads import _6176
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BeltDriveLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveLoadCase',)


class BeltDriveLoadCase(_6176.SpecialisedAssemblyLoadCase):
    '''BeltDriveLoadCase

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def pre_tension(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PreTension' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PreTension) if self.wrapped.PreTension else None

    @pre_tension.setter
    def pre_tension(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.PreTension = value

    @property
    def assembly_design(self) -> '_2111.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
