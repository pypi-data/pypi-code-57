'''_1069.py

GearMeshDesignAnalysis
'''


from mastapy.gears.analysis import _1071, _351
from mastapy._internal import constructor
from mastapy.gears.gear_twod_fe_analysis import _905
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1029, _1028
from mastapy.gears.load_case.worm import _887
from mastapy.gears.load_case.face import _889
from mastapy.gears.load_case.cylindrical import _891
from mastapy.gears.load_case.conical import _897
from mastapy.gears.load_case.concept import _899
from mastapy.gears.load_case.bevel import _901
from mastapy.gears.manufacturing.cylindrical import _615, _614, _609
from mastapy.gears.manufacturing.bevel import (
    _796, _799, _810, _816,
    _811
)
from mastapy.gears.ltca.cylindrical import _870
from mastapy.gears.ltca.conical import _879
from mastapy.gears.gear_designs.face import _958
from mastapy.gears.fe_model.cylindrical import _1118
from mastapy.gears.fe_model.conical import _1120
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_DESIGN_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearMeshDesignAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshDesignAnalysis',)


class GearMeshDesignAnalysis(_351.AbstractGearMeshAnalysis):
    '''GearMeshDesignAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_DESIGN_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshDesignAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_a(self) -> '_1071.GearDesignAnalysis':
        '''GearDesignAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.GearDesignAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_tiff_analysis(self) -> '_905.CylindricalGearTIFFAnalysis':
        '''CylindricalGearTIFFAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'CylindricalGearTIFFAnalysis':
            raise CastException('Failed to cast gear_a to CylindricalGearTIFFAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_905.CylindricalGearTIFFAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_micro_geometry_duty_cycle(self) -> '_1029.CylindricalGearMicroGeometryDutyCycle':
        '''CylindricalGearMicroGeometryDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'CylindricalGearMicroGeometryDutyCycle':
            raise CastException('Failed to cast gear_a to CylindricalGearMicroGeometryDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_1029.CylindricalGearMicroGeometryDutyCycle)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_worm_gear_load_case(self) -> '_887.WormGearLoadCase':
        '''WormGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'WormGearLoadCase':
            raise CastException('Failed to cast gear_a to WormGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_887.WormGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_face_gear_load_case(self) -> '_889.FaceGearLoadCase':
        '''FaceGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'FaceGearLoadCase':
            raise CastException('Failed to cast gear_a to FaceGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_889.FaceGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_load_case(self) -> '_891.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'CylindricalGearLoadCase':
            raise CastException('Failed to cast gear_a to CylindricalGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_891.CylindricalGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_load_case(self) -> '_897.ConicalGearLoadCase':
        '''ConicalGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'ConicalGearLoadCase':
            raise CastException('Failed to cast gear_a to ConicalGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_897.ConicalGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_concept_gear_load_case(self) -> '_899.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'ConceptGearLoadCase':
            raise CastException('Failed to cast gear_a to ConceptGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_899.ConceptGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_bevel_load_case(self) -> '_901.BevelLoadCase':
        '''BevelLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'BevelLoadCase':
            raise CastException('Failed to cast gear_a to BevelLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_901.BevelLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_manufactured_gear_load_case(self) -> '_615.CylindricalManufacturedGearLoadCase':
        '''CylindricalManufacturedGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'CylindricalManufacturedGearLoadCase':
            raise CastException('Failed to cast gear_a to CylindricalManufacturedGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_615.CylindricalManufacturedGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_manufacturing_analysis(self) -> '_796.ConicalGearManufacturingAnalysis':
        '''ConicalGearManufacturingAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'ConicalGearManufacturingAnalysis':
            raise CastException('Failed to cast gear_a to ConicalGearManufacturingAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_796.ConicalGearManufacturingAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_load_distribution_analysis(self) -> '_870.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'CylindricalGearLoadDistributionAnalysis':
            raise CastException('Failed to cast gear_a to CylindricalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_870.CylindricalGearLoadDistributionAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_load_distribution_analysis(self) -> '_879.ConicalGearLoadDistributionAnalysis':
        '''ConicalGearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'ConicalGearLoadDistributionAnalysis':
            raise CastException('Failed to cast gear_a to ConicalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_879.ConicalGearLoadDistributionAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_manufactured_gear_duty_cycle(self) -> '_614.CylindricalManufacturedGearDutyCycle':
        '''CylindricalManufacturedGearDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'CylindricalManufacturedGearDutyCycle':
            raise CastException('Failed to cast gear_a to CylindricalManufacturedGearDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_614.CylindricalManufacturedGearDutyCycle)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_manufacturing_config(self) -> '_609.CylindricalGearManufacturingConfig':
        '''CylindricalGearManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'CylindricalGearManufacturingConfig':
            raise CastException('Failed to cast gear_a to CylindricalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_609.CylindricalGearManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_face_gear_micro_geometry(self) -> '_958.FaceGearMicroGeometry':
        '''FaceGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'FaceGearMicroGeometry':
            raise CastException('Failed to cast gear_a to FaceGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_958.FaceGearMicroGeometry)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_micro_geometry(self) -> '_1028.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'CylindricalGearMicroGeometry':
            raise CastException('Failed to cast gear_a to CylindricalGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_1028.CylindricalGearMicroGeometry)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_micro_geometry_config(self) -> '_799.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'ConicalGearMicroGeometryConfig':
            raise CastException('Failed to cast gear_a to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_799.ConicalGearMicroGeometryConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_pinion_manufacturing_config(self) -> '_810.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'ConicalPinionManufacturingConfig':
            raise CastException('Failed to cast gear_a to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_810.ConicalPinionManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_wheel_manufacturing_config(self) -> '_816.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'ConicalWheelManufacturingConfig':
            raise CastException('Failed to cast gear_a to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_816.ConicalWheelManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_pinion_micro_geometry_config(self) -> '_811.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'ConicalPinionMicroGeometryConfig':
            raise CastException('Failed to cast gear_a to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_811.ConicalPinionMicroGeometryConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_fe_model(self) -> '_1118.CylindricalGearFEModel':
        '''CylindricalGearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'CylindricalGearFEModel':
            raise CastException('Failed to cast gear_a to CylindricalGearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_1118.CylindricalGearFEModel)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_fe_model(self) -> '_1120.ConicalGearFEModel':
        '''ConicalGearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearA.__class__.__qualname__ != 'ConicalGearFEModel':
            raise CastException('Failed to cast gear_a to ConicalGearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_1120.ConicalGearFEModel)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_b(self) -> '_1071.GearDesignAnalysis':
        '''GearDesignAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1071.GearDesignAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_tiff_analysis(self) -> '_905.CylindricalGearTIFFAnalysis':
        '''CylindricalGearTIFFAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'CylindricalGearTIFFAnalysis':
            raise CastException('Failed to cast gear_b to CylindricalGearTIFFAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_905.CylindricalGearTIFFAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_micro_geometry_duty_cycle(self) -> '_1029.CylindricalGearMicroGeometryDutyCycle':
        '''CylindricalGearMicroGeometryDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'CylindricalGearMicroGeometryDutyCycle':
            raise CastException('Failed to cast gear_b to CylindricalGearMicroGeometryDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_1029.CylindricalGearMicroGeometryDutyCycle)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_worm_gear_load_case(self) -> '_887.WormGearLoadCase':
        '''WormGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'WormGearLoadCase':
            raise CastException('Failed to cast gear_b to WormGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_887.WormGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_face_gear_load_case(self) -> '_889.FaceGearLoadCase':
        '''FaceGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'FaceGearLoadCase':
            raise CastException('Failed to cast gear_b to FaceGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_889.FaceGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_load_case(self) -> '_891.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'CylindricalGearLoadCase':
            raise CastException('Failed to cast gear_b to CylindricalGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_891.CylindricalGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_load_case(self) -> '_897.ConicalGearLoadCase':
        '''ConicalGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'ConicalGearLoadCase':
            raise CastException('Failed to cast gear_b to ConicalGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_897.ConicalGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_concept_gear_load_case(self) -> '_899.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'ConceptGearLoadCase':
            raise CastException('Failed to cast gear_b to ConceptGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_899.ConceptGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_bevel_load_case(self) -> '_901.BevelLoadCase':
        '''BevelLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'BevelLoadCase':
            raise CastException('Failed to cast gear_b to BevelLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_901.BevelLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_manufactured_gear_load_case(self) -> '_615.CylindricalManufacturedGearLoadCase':
        '''CylindricalManufacturedGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'CylindricalManufacturedGearLoadCase':
            raise CastException('Failed to cast gear_b to CylindricalManufacturedGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_615.CylindricalManufacturedGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_manufacturing_analysis(self) -> '_796.ConicalGearManufacturingAnalysis':
        '''ConicalGearManufacturingAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'ConicalGearManufacturingAnalysis':
            raise CastException('Failed to cast gear_b to ConicalGearManufacturingAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_796.ConicalGearManufacturingAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_load_distribution_analysis(self) -> '_870.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'CylindricalGearLoadDistributionAnalysis':
            raise CastException('Failed to cast gear_b to CylindricalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_870.CylindricalGearLoadDistributionAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_load_distribution_analysis(self) -> '_879.ConicalGearLoadDistributionAnalysis':
        '''ConicalGearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'ConicalGearLoadDistributionAnalysis':
            raise CastException('Failed to cast gear_b to ConicalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_879.ConicalGearLoadDistributionAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_manufactured_gear_duty_cycle(self) -> '_614.CylindricalManufacturedGearDutyCycle':
        '''CylindricalManufacturedGearDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'CylindricalManufacturedGearDutyCycle':
            raise CastException('Failed to cast gear_b to CylindricalManufacturedGearDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_614.CylindricalManufacturedGearDutyCycle)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_manufacturing_config(self) -> '_609.CylindricalGearManufacturingConfig':
        '''CylindricalGearManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'CylindricalGearManufacturingConfig':
            raise CastException('Failed to cast gear_b to CylindricalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_609.CylindricalGearManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_face_gear_micro_geometry(self) -> '_958.FaceGearMicroGeometry':
        '''FaceGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'FaceGearMicroGeometry':
            raise CastException('Failed to cast gear_b to FaceGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_958.FaceGearMicroGeometry)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_micro_geometry(self) -> '_1028.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'CylindricalGearMicroGeometry':
            raise CastException('Failed to cast gear_b to CylindricalGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_1028.CylindricalGearMicroGeometry)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_micro_geometry_config(self) -> '_799.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'ConicalGearMicroGeometryConfig':
            raise CastException('Failed to cast gear_b to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_799.ConicalGearMicroGeometryConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_pinion_manufacturing_config(self) -> '_810.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'ConicalPinionManufacturingConfig':
            raise CastException('Failed to cast gear_b to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_810.ConicalPinionManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_wheel_manufacturing_config(self) -> '_816.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'ConicalWheelManufacturingConfig':
            raise CastException('Failed to cast gear_b to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_816.ConicalWheelManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_pinion_micro_geometry_config(self) -> '_811.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'ConicalPinionMicroGeometryConfig':
            raise CastException('Failed to cast gear_b to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_811.ConicalPinionMicroGeometryConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_fe_model(self) -> '_1118.CylindricalGearFEModel':
        '''CylindricalGearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'CylindricalGearFEModel':
            raise CastException('Failed to cast gear_b to CylindricalGearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_1118.CylindricalGearFEModel)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_fe_model(self) -> '_1120.ConicalGearFEModel':
        '''ConicalGearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.GearB.__class__.__qualname__ != 'ConicalGearFEModel':
            raise CastException('Failed to cast gear_b to ConicalGearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_1120.ConicalGearFEModel)(self.wrapped.GearB) if self.wrapped.GearB else None
