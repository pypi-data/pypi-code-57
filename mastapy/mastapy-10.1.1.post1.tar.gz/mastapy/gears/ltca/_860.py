'''_860.py

GearMeshLoadDistributionAtRotation
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.ltca import _861
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_LOAD_DISTRIBUTION_AT_ROTATION = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearMeshLoadDistributionAtRotation')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshLoadDistributionAtRotation',)


class GearMeshLoadDistributionAtRotation(_1.APIBase):
    '''GearMeshLoadDistributionAtRotation

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_LOAD_DISTRIBUTION_AT_ROTATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshLoadDistributionAtRotation.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def mesh_stiffness(self) -> 'float':
        '''float: 'MeshStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshStiffness

    @property
    def index(self) -> 'int':
        '''int: 'Index' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Index

    @property
    def transmission_error(self) -> 'float':
        '''float: 'TransmissionError' is the original name of this property.'''

        return self.wrapped.TransmissionError

    @transmission_error.setter
    def transmission_error(self, value: 'float'):
        self.wrapped.TransmissionError = float(value) if value else 0.0

    @property
    def number_of_potentially_loaded_teeth(self) -> 'int':
        '''int: 'NumberOfPotentiallyLoadedTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfPotentiallyLoadedTeeth

    @property
    def number_of_loaded_teeth(self) -> 'int':
        '''int: 'NumberOfLoadedTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfLoadedTeeth

    @property
    def loaded_contact_lines(self) -> 'List[_861.GearMeshLoadedContactLine]':
        '''List[GearMeshLoadedContactLine]: 'LoadedContactLines' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadedContactLines, constructor.new(_861.GearMeshLoadedContactLine))
        return value
