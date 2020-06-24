'''_718.py

CylindricalManufacturedRealGearInMesh
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MANUFACTURED_REAL_GEAR_IN_MESH = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'CylindricalManufacturedRealGearInMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalManufacturedRealGearInMesh',)


class CylindricalManufacturedRealGearInMesh(_1.APIBase):
    '''CylindricalManufacturedRealGearInMesh

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_MANUFACTURED_REAL_GEAR_IN_MESH
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalManufacturedRealGearInMesh.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def transverse_contact_ratio(self) -> 'float':
        '''float: 'TransverseContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseContactRatio

    @property
    def active_tip_diameter(self) -> 'float':
        '''float: 'ActiveTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ActiveTipDiameter

    @property
    def active_root_diameter(self) -> 'float':
        '''float: 'ActiveRootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ActiveRootDiameter

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name
