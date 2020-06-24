'''_750.py

CylindricalGearGrindingWorm
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _767, _769, _764
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters import _755
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_GRINDING_WORM = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearGrindingWorm')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearGrindingWorm',)


class CylindricalGearGrindingWorm(_755.CylindricalGearRackDesign):
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
    def nominal_worm_grinder_shape(self) -> '_767.CylindricalGearWormGrinderShape':
        '''CylindricalGearWormGrinderShape: 'NominalWormGrinderShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_767.CylindricalGearWormGrinderShape)(self.wrapped.NominalWormGrinderShape) if self.wrapped.NominalWormGrinderShape else None

    @property
    def nominal_rack_shape(self) -> '_769.RackShape':
        '''RackShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_769.RackShape)(self.wrapped.NominalRackShape) if self.wrapped.NominalRackShape else None

    @property
    def nominal_rack_shape_of_type_cylindrical_gear_hob_shape(self) -> '_764.CylindricalGearHobShape':
        '''CylindricalGearHobShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.NominalRackShape.__class__.__qualname__ != 'CylindricalGearHobShape':
            raise CastException('Failed to cast nominal_rack_shape to CylindricalGearHobShape. Expected: {}.'.format(self.wrapped.NominalRackShape.__class__.__qualname__))

        return constructor.new(_764.CylindricalGearHobShape)(self.wrapped.NominalRackShape) if self.wrapped.NominalRackShape else None

    @property
    def nominal_rack_shape_of_type_cylindrical_gear_worm_grinder_shape(self) -> '_767.CylindricalGearWormGrinderShape':
        '''CylindricalGearWormGrinderShape: 'NominalRackShape' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.NominalRackShape.__class__.__qualname__ != 'CylindricalGearWormGrinderShape':
            raise CastException('Failed to cast nominal_rack_shape to CylindricalGearWormGrinderShape. Expected: {}.'.format(self.wrapped.NominalRackShape.__class__.__qualname__))

        return constructor.new(_767.CylindricalGearWormGrinderShape)(self.wrapped.NominalRackShape) if self.wrapped.NominalRackShape else None
