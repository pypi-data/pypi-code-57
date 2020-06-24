'''_755.py

CylindricalGearRackDesign
'''


from mastapy._internal import constructor, conversion
from mastapy.gears import _305, _321
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _769, _764, _767
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters import _751
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_RACK_DESIGN = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearRackDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearRackDesign',)


class CylindricalGearRackDesign(_751.CylindricalGearRealCutterDesign):
    '''CylindricalGearRackDesign

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_RACK_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearRackDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def addendum(self) -> 'float':
        '''float: 'Addendum' is the original name of this property.'''

        return self.wrapped.Addendum

    @addendum.setter
    def addendum(self, value: 'float'):
        self.wrapped.Addendum = float(value) if value else 0.0

    @property
    def addendum_keeping_dedendum_constant(self) -> 'float':
        '''float: 'AddendumKeepingDedendumConstant' is the original name of this property.'''

        return self.wrapped.AddendumKeepingDedendumConstant

    @addendum_keeping_dedendum_constant.setter
    def addendum_keeping_dedendum_constant(self, value: 'float'):
        self.wrapped.AddendumKeepingDedendumConstant = float(value) if value else 0.0

    @property
    def addendum_factor(self) -> 'float':
        '''float: 'AddendumFactor' is the original name of this property.'''

        return self.wrapped.AddendumFactor

    @addendum_factor.setter
    def addendum_factor(self, value: 'float'):
        self.wrapped.AddendumFactor = float(value) if value else 0.0

    @property
    def dedendum(self) -> 'float':
        '''float: 'Dedendum' is the original name of this property.'''

        return self.wrapped.Dedendum

    @dedendum.setter
    def dedendum(self, value: 'float'):
        self.wrapped.Dedendum = float(value) if value else 0.0

    @property
    def dedendum_factor(self) -> 'float':
        '''float: 'DedendumFactor' is the original name of this property.'''

        return self.wrapped.DedendumFactor

    @dedendum_factor.setter
    def dedendum_factor(self, value: 'float'):
        self.wrapped.DedendumFactor = float(value) if value else 0.0

    @property
    def tip_diameter(self) -> 'float':
        '''float: 'TipDiameter' is the original name of this property.'''

        return self.wrapped.TipDiameter

    @tip_diameter.setter
    def tip_diameter(self, value: 'float'):
        self.wrapped.TipDiameter = float(value) if value else 0.0

    @property
    def number_of_threads(self) -> 'int':
        '''int: 'NumberOfThreads' is the original name of this property.'''

        return self.wrapped.NumberOfThreads

    @number_of_threads.setter
    def number_of_threads(self, value: 'int'):
        self.wrapped.NumberOfThreads = int(value) if value else 0

    @property
    def effective_length(self) -> 'float':
        '''float: 'EffectiveLength' is the original name of this property.'''

        return self.wrapped.EffectiveLength

    @effective_length.setter
    def effective_length(self, value: 'float'):
        self.wrapped.EffectiveLength = float(value) if value else 0.0

    @property
    def hand(self) -> '_305.Hand':
        '''Hand: 'Hand' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Hand)
        return constructor.new(_305.Hand)(value) if value else None

    @hand.setter
    def hand(self, value: '_305.Hand'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Hand = value

    @property
    def worm_type(self) -> '_321.WormType':
        '''WormType: 'WormType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.WormType)
        return constructor.new(_321.WormType)(value) if value else None

    @worm_type.setter
    def worm_type(self, value: '_321.WormType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.WormType = value

    @property
    def flat_tip_width(self) -> 'float':
        '''float: 'FlatTipWidth' is the original name of this property.'''

        return self.wrapped.FlatTipWidth

    @flat_tip_width.setter
    def flat_tip_width(self, value: 'float'):
        self.wrapped.FlatTipWidth = float(value) if value else 0.0

    @property
    def flat_root_width(self) -> 'float':
        '''float: 'FlatRootWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FlatRootWidth

    @property
    def use_maximum_edge_radius(self) -> 'bool':
        '''bool: 'UseMaximumEdgeRadius' is the original name of this property.'''

        return self.wrapped.UseMaximumEdgeRadius

    @use_maximum_edge_radius.setter
    def use_maximum_edge_radius(self, value: 'bool'):
        self.wrapped.UseMaximumEdgeRadius = bool(value) if value else False

    @property
    def edge_radius(self) -> 'float':
        '''float: 'EdgeRadius' is the original name of this property.'''

        return self.wrapped.EdgeRadius

    @edge_radius.setter
    def edge_radius(self, value: 'float'):
        self.wrapped.EdgeRadius = float(value) if value else 0.0

    @property
    def edge_height(self) -> 'float':
        '''float: 'EdgeHeight' is the original name of this property.'''

        return self.wrapped.EdgeHeight

    @edge_height.setter
    def edge_height(self, value: 'float'):
        self.wrapped.EdgeHeight = float(value) if value else 0.0

    @property
    def whole_depth(self) -> 'float':
        '''float: 'WholeDepth' is the original name of this property.'''

        return self.wrapped.WholeDepth

    @whole_depth.setter
    def whole_depth(self, value: 'float'):
        self.wrapped.WholeDepth = float(value) if value else 0.0

    @property
    def normal_thickness(self) -> 'float':
        '''float: 'NormalThickness' is the original name of this property.'''

        return self.wrapped.NormalThickness

    @normal_thickness.setter
    def normal_thickness(self, value: 'float'):
        self.wrapped.NormalThickness = float(value) if value else 0.0

    @property
    def reference_diameter(self) -> 'float':
        '''float: 'ReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReferenceDiameter

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
