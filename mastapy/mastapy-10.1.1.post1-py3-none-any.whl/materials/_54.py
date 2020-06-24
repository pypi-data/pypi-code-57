'''_54.py

ComponentMaterialDatabase
'''


from mastapy.utility.databases import _1341
from mastapy.materials import _76
from mastapy._internal.python_net import python_net_import

_COMPONENT_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Materials', 'ComponentMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentMaterialDatabase',)


class ComponentMaterialDatabase(_1341.NamedDatabase['_76.Material']):
    '''ComponentMaterialDatabase

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
