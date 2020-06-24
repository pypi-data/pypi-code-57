'''_644.py

SuitableCutterSetup
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutters import _730
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _731
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SUITABLE_CUTTER_SETUP = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'SuitableCutterSetup')


__docformat__ = 'restructuredtext en'
__all__ = ('SuitableCutterSetup',)


class SuitableCutterSetup(_1.APIBase):
    '''SuitableCutterSetup

    This is a mastapy class.
    '''

    TYPE = _SUITABLE_CUTTER_SETUP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SuitableCutterSetup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def rough_cutter_creation_settings(self) -> '_730.RoughCutterCreationSettings':
        '''RoughCutterCreationSettings: 'RoughCutterCreationSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_730.RoughCutterCreationSettings)(self.wrapped.RoughCutterCreationSettings) if self.wrapped.RoughCutterCreationSettings else None

    @property
    def tool_clearances(self) -> '_731.ManufacturingOperationConstraints':
        '''ManufacturingOperationConstraints: 'ToolClearances' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_731.ManufacturingOperationConstraints)(self.wrapped.ToolClearances) if self.wrapped.ToolClearances else None
