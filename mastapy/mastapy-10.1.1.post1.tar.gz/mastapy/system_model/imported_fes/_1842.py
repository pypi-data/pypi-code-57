'''_1842.py

BearingRaceNodeLink
'''


from mastapy._internal import constructor, conversion
from mastapy.system_model.imported_fes import _1843
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_BEARING_RACE_NODE_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'BearingRaceNodeLink')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingRaceNodeLink',)


class BearingRaceNodeLink(_1.APIBase):
    '''BearingRaceNodeLink

    This is a mastapy class.
    '''

    TYPE = _BEARING_RACE_NODE_LINK
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingRaceNodeLink.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def race_position(self) -> '_1843.BearingRacePosition':
        '''BearingRacePosition: 'RacePosition' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.RacePosition)
        return constructor.new(_1843.BearingRacePosition)(value) if value else None
