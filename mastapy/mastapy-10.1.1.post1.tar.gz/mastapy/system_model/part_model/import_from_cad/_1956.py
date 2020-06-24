'''_1956.py

ConnectorFromCAD
'''


from mastapy.system_model.part_model.import_from_cad import _1962, _1963
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_CONNECTOR_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'ConnectorFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorFromCAD',)


class ConnectorFromCAD(_1963.MountableComponentFromCAD):
    '''ConnectorFromCAD

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_FROM_CAD
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorFromCAD.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def mounting(self) -> '_1962.HousedOrMounted':
        '''HousedOrMounted: 'Mounting' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Mounting)
        return constructor.new(_1962.HousedOrMounted)(value) if value else None

    @mounting.setter
    def mounting(self, value: '_1962.HousedOrMounted'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Mounting = value
