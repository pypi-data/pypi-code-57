'''_510.py

CylindricalGearGrindingWorm
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _530, _532, _527
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters import _514
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_GRINDING_WORM = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearGrindingWorm')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearGrindingWorm',)


class CylindricalGearGrindingWorm(_514.CylindricalGearRackDesign):
    '''CylindricalGearGrindingWorm

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_GRINDING_WORM

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearGrindingWorm.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def clearance_coefficient(self) -> 'float':
        '''float: 'ClearanceCoefficient' is the original name of this property.'''

        return self.wrapped.ClearanceCoefficient

    @clearance_coefficient.setter
    def clearance_coefficient(self, value: 'float'):
        self.wrapped.ClearanceCoefficient = float(value) if value else 0.0

    @property
    def flat_tip_width(self) -> 'float':
        '''float: 'FlatTipWidth' is the original name of this property.'''

        return self.wrapped.FlatTipWidth

    @flat_tip_width.setter
    def flat_tip_width(self, value: 'float'):
        self.wrapped.FlatTipWidth = float(value) if value else 0.0

    @property
    def edge_height(self) -> 'float':
        '''float: 'EdgeHeight' is the original name of this property.'''

        return self.wrapped.EdgeHeight

    @edge_height.setter
    def edge_height(self, value: 'float'):
        self.wrapped.EdgeHeight = float(value) if value else 0.0

    @property
    def has_tolerances(self) -> 'bool':
        '''bool: 'HasTolerances' is the original name of this property.'''

        return self.wrapped.HasTolerances

    @has_tolerances.setter
    def has_tolerances(self, value: 'bool'):
        self.wrapped.HasTolerances = bool(value) if value else False

    @property
    def nominal_worm_grinder_shape(self) -> '_530.CylindricalGearWormGrinderShape':
        '''CylindricalGearWormGrinderShape: 'NominalWormGrinderShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_530.CylindricalGearWormGrinderShape)(self.wrapped.NominalWormGrinderShape) if self.wrapped.NominalWormGrinderShape else None

    @property
    def nominal_rack_shape(self) -> '_532.RackShape':
        '''RackShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_532.RackShape)(self.wrapped.NominalRackShape) if self.wrapped.NominalRackShape else None

    @property
    def nominal_rack_shape_of_type_cylindrical_gear_hob_shape(self) -> '_527.CylindricalGearHobShape':
        '''CylindricalGearHobShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _527.CylindricalGearHobShape.TYPE not in self.wrapped.NominalRackShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_rack_shape to CylindricalGearHobShape. Expected: {}.'.format(self.wrapped.NominalRackShape.__class__.__qualname__))

        return constructor.new(_527.CylindricalGearHobShape)(self.wrapped.NominalRackShape) if self.wrapped.NominalRackShape else None

    @property
    def nominal_rack_shape_of_type_cylindrical_gear_worm_grinder_shape(self) -> '_530.CylindricalGearWormGrinderShape':
        '''CylindricalGearWormGrinderShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _530.CylindricalGearWormGrinderShape.TYPE not in self.wrapped.NominalRackShape.__class__.__mro__:
            raise CastException('Failed to cast nominal_rack_shape to CylindricalGearWormGrinderShape. Expected: {}.'.format(self.wrapped.NominalRackShape.__class__.__qualname__))

        return constructor.new(_530.CylindricalGearWormGrinderShape)(self.wrapped.NominalRackShape) if self.wrapped.NominalRackShape else None
