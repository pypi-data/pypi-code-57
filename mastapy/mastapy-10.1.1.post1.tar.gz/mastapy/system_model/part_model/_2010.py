'''_2010.py

PlanetCarrier
'''


from typing import List, Optional

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.part_model import _1983, _2003, _2006
from mastapy.system_model.connections_and_sockets import _1849
from mastapy.system_model.part_model.shaft_model import _2022
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrier',)


class PlanetCarrier(_2006.MountableComponent):
    '''PlanetCarrier

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrier.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def length(self) -> 'float':
        '''float: 'Length' is the original name of this property.'''

        return self.wrapped.Length

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def planetary_load_sharing_agma_application_level(self) -> '_1983.AGMALoadSharingTableApplicationLevel':
        '''AGMALoadSharingTableApplicationLevel: 'PlanetaryLoadSharingAGMAApplicationLevel' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.PlanetaryLoadSharingAGMAApplicationLevel)
        return constructor.new(_1983.AGMALoadSharingTableApplicationLevel)(value) if value else None

    @planetary_load_sharing_agma_application_level.setter
    def planetary_load_sharing_agma_application_level(self, value: '_1983.AGMALoadSharingTableApplicationLevel'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PlanetaryLoadSharingAGMAApplicationLevel = value

    @property
    def planetary_load_sharing(self) -> '_2003.LoadSharingModes':
        '''LoadSharingModes: 'PlanetaryLoadSharing' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.PlanetaryLoadSharing)
        return constructor.new(_2003.LoadSharingModes)(value) if value else None

    @planetary_load_sharing.setter
    def planetary_load_sharing(self, value: '_2003.LoadSharingModes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PlanetaryLoadSharing = value

    @property
    def number_of_planetary_sockets(self) -> 'int':
        '''int: 'NumberOfPlanetarySockets' is the original name of this property.'''

        return self.wrapped.NumberOfPlanetarySockets

    @number_of_planetary_sockets.setter
    def number_of_planetary_sockets(self, value: 'int'):
        self.wrapped.NumberOfPlanetarySockets = int(value) if value else 0

    @property
    def planetary_sockets(self) -> 'List[_1849.PlanetarySocket]':
        '''List[PlanetarySocket]: 'PlanetarySockets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetarySockets, constructor.new(_1849.PlanetarySocket))
        return value

    def attach_carrier_shaft(self, shaft: '_2022.Shaft', offset: Optional['float'] = float('nan')):
        ''' 'AttachCarrierShaft' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)
        '''

        offset = float(offset)
        self.wrapped.AttachCarrierShaft(shaft.wrapped if shaft else None, offset if offset else 0.0)

    def attach_pin_shaft(self, shaft: '_2022.Shaft', offset: Optional['float'] = float('nan')):
        ''' 'AttachPinShaft' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)
        '''

        offset = float(offset)
        self.wrapped.AttachPinShaft(shaft.wrapped if shaft else None, offset if offset else 0.0)
