'''_715.py

GearSetDesign
'''


from typing import Callable, List, Optional

from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy.scripting import _6504
from mastapy.gears import _130
from mastapy.gears.fe_model import _934
from mastapy.gears.fe_model.cylindrical import _937
from mastapy._internal.cast_exception import CastException
from mastapy.gears.fe_model.conical import _940
from mastapy.gears.gear_designs import _712, _713

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'GearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetDesign',)


class GearSetDesign(_713.GearDesignComponent):
    '''GearSetDesign

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def long_name(self) -> 'str':
        '''str: 'LongName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LongName

    @property
    def fe_model(self) -> 'str':
        '''str: 'FEModel' is the original name of this property.'''

        return self.wrapped.FEModel.SelectedItemName

    @fe_model.setter
    def fe_model(self, value: 'str'):
        self.wrapped.FEModel.SetSelectedItem(str(value) if value else None)

    @property
    def create_new_fe_model(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CreateNewFEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateNewFEModel

    @property
    def create_new_tifffe_model(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CreateNewTIFFFEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateNewTIFFFEModel

    @property
    def gear_set_drawing(self) -> '_6504.SMTBitmap':
        '''SMTBitmap: 'GearSetDrawing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6504.SMTBitmap)(self.wrapped.GearSetDrawing) if self.wrapped.GearSetDrawing else None

    @property
    def mass(self) -> 'float':
        '''float: 'Mass' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Mass

    @property
    def name_including_tooth_numbers(self) -> 'str':
        '''str: 'NameIncludingToothNumbers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NameIncludingToothNumbers

    @property
    def required_safety_factor_for_contact(self) -> 'float':
        '''float: 'RequiredSafetyFactorForContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RequiredSafetyFactorForContact

    @property
    def required_safety_factor_for_bending(self) -> 'float':
        '''float: 'RequiredSafetyFactorForBending' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RequiredSafetyFactorForBending

    @property
    def required_safety_factor_for_static_contact(self) -> 'float':
        '''float: 'RequiredSafetyFactorForStaticContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RequiredSafetyFactorForStaticContact

    @property
    def required_safety_factor_for_static_bending(self) -> 'float':
        '''float: 'RequiredSafetyFactorForStaticBending' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RequiredSafetyFactorForStaticBending

    @property
    def largest_mesh_ratio(self) -> 'float':
        '''float: 'LargestMeshRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LargestMeshRatio

    @property
    def transverse_and_axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseAndAxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseAndAxialContactRatioRatingForNVH

    @property
    def transverse_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseContactRatioRatingForNVH

    @property
    def axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'AxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialContactRatioRatingForNVH

    @property
    def smallest_number_of_teeth(self) -> 'int':
        '''int: 'SmallestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SmallestNumberOfTeeth

    @property
    def largest_number_of_teeth(self) -> 'int':
        '''int: 'LargestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LargestNumberOfTeeth

    @property
    def transmission_properties_gears(self) -> '_130.GearSetDesignGroup':
        '''GearSetDesignGroup: 'TransmissionPropertiesGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_130.GearSetDesignGroup)(self.wrapped.TransmissionPropertiesGears) if self.wrapped.TransmissionPropertiesGears else None

    @property
    def ltcafe_model(self) -> '_934.GearSetFEModel':
        '''GearSetFEModel: 'LTCAFEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_934.GearSetFEModel)(self.wrapped.LTCAFEModel) if self.wrapped.LTCAFEModel else None

    @property
    def ltcafe_model_of_type_cylindrical_gear_set_fe_model(self) -> '_937.CylindricalGearSetFEModel':
        '''CylindricalGearSetFEModel: 'LTCAFEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _937.CylindricalGearSetFEModel.TYPE not in self.wrapped.LTCAFEModel.__class__.__mro__:
            raise CastException('Failed to cast ltcafe_model to CylindricalGearSetFEModel. Expected: {}.'.format(self.wrapped.LTCAFEModel.__class__.__qualname__))

        return constructor.new(_937.CylindricalGearSetFEModel)(self.wrapped.LTCAFEModel) if self.wrapped.LTCAFEModel else None

    @property
    def ltcafe_model_of_type_conical_set_fe_model(self) -> '_940.ConicalSetFEModel':
        '''ConicalSetFEModel: 'LTCAFEModel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _940.ConicalSetFEModel.TYPE not in self.wrapped.LTCAFEModel.__class__.__mro__:
            raise CastException('Failed to cast ltcafe_model to ConicalSetFEModel. Expected: {}.'.format(self.wrapped.LTCAFEModel.__class__.__qualname__))

        return constructor.new(_940.ConicalSetFEModel)(self.wrapped.LTCAFEModel) if self.wrapped.LTCAFEModel else None

    @property
    def gears(self) -> 'List[_712.GearDesign]':
        '''List[GearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_712.GearDesign))
        return value

    def copy(self, include_fe: Optional['bool'] = False) -> 'GearSetDesign':
        ''' 'Copy' is the original name of this method.

        Args:
            include_fe (bool, optional)

        Returns:
            mastapy.gears.gear_designs.GearSetDesign
        '''

        include_fe = bool(include_fe)
        method_result = self.wrapped.Copy(include_fe if include_fe else False)
        return constructor.new(GearSetDesign)(method_result) if method_result else None
