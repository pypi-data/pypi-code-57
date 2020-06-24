'''_1036.py

BoltedJointMaterialDatabase
'''


from typing import Generic, TypeVar

from mastapy.utility.databases import _1341
from mastapy.bolts import _1035
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Bolts', 'BoltedJointMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointMaterialDatabase',)


T = TypeVar('T', bound='_1035.BoltedJointMaterial')


class BoltedJointMaterialDatabase(_1341.NamedDatabase['T'], Generic[T]):
    '''BoltedJointMaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _BOLTED_JOINT_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
