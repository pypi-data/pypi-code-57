'''_2038.py

CylindricalGearLinearTrainCreationOptions
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_LINEAR_TRAIN_CREATION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.CreationOptions', 'CylindricalGearLinearTrainCreationOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearLinearTrainCreationOptions',)


class CylindricalGearLinearTrainCreationOptions(_1.APIBase):
    '''CylindricalGearLinearTrainCreationOptions

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_LINEAR_TRAIN_CREATION_OPTIONS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearLinearTrainCreationOptions.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def number_of_gears(self) -> 'int':
        '''int: 'NumberOfGears' is the original name of this property.'''

        return self.wrapped.NumberOfGears

    @number_of_gears.setter
    def number_of_gears(self, value: 'int'):
        self.wrapped.NumberOfGears = int(value) if value else 0
