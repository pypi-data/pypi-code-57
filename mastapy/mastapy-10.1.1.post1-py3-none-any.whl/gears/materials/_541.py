'''_541.py

PlasticSNCurve
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.materials import _273, _270, _271
from mastapy.gears.materials import _604
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PLASTIC_SN_CURVE = python_net_import('SMT.MastaAPI.Gears.Materials', 'PlasticSNCurve')


__docformat__ = 'restructuredtext en'
__all__ = ('PlasticSNCurve',)


class PlasticSNCurve(_1.APIBase):
    '''PlasticSNCurve

    This is a mastapy class.
    '''

    TYPE = _PLASTIC_SN_CURVE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlasticSNCurve.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def flank_temperature(self) -> 'float':
        '''float: 'FlankTemperature' is the original name of this property.'''

        return self.wrapped.FlankTemperature

    @flank_temperature.setter
    def flank_temperature(self, value: 'float'):
        self.wrapped.FlankTemperature = float(value) if value else 0.0

    @property
    def note_1(self) -> 'str':
        '''str: 'Note1' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Note1

    @property
    def note_2(self) -> 'str':
        '''str: 'Note2' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Note2

    @property
    def root_temperature(self) -> 'float':
        '''float: 'RootTemperature' is the original name of this property.'''

        return self.wrapped.RootTemperature

    @root_temperature.setter
    def root_temperature(self, value: 'float'):
        self.wrapped.RootTemperature = float(value) if value else 0.0

    @property
    def life_cycles(self) -> 'float':
        '''float: 'LifeCycles' is the original name of this property.'''

        return self.wrapped.LifeCycles

    @life_cycles.setter
    def life_cycles(self, value: 'float'):
        self.wrapped.LifeCycles = float(value) if value else 0.0

    @property
    def nominal_stress_number_bending(self) -> 'float':
        '''float: 'NominalStressNumberBending' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NominalStressNumberBending

    @property
    def allowable_stress_number_bending(self) -> 'float':
        '''float: 'AllowableStressNumberBending' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AllowableStressNumberBending

    @property
    def allowable_stress_number_contact(self) -> 'float':
        '''float: 'AllowableStressNumberContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AllowableStressNumberContact

    @property
    def lubricant(self) -> '_273.VDI2736LubricantType':
        '''VDI2736LubricantType: 'Lubricant' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Lubricant)
        return constructor.new(_273.VDI2736LubricantType)(value) if value else None

    @lubricant.setter
    def lubricant(self, value: '_273.VDI2736LubricantType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Lubricant = value

    @property
    def number_of_rows_in_the_bending_sn_table(self) -> 'int':
        '''int: 'NumberOfRowsInTheBendingSNTable' is the original name of this property.'''

        return self.wrapped.NumberOfRowsInTheBendingSNTable

    @number_of_rows_in_the_bending_sn_table.setter
    def number_of_rows_in_the_bending_sn_table(self, value: 'int'):
        self.wrapped.NumberOfRowsInTheBendingSNTable = int(value) if value else 0

    @property
    def number_of_rows_in_the_contact_sn_table(self) -> 'int':
        '''int: 'NumberOfRowsInTheContactSNTable' is the original name of this property.'''

        return self.wrapped.NumberOfRowsInTheContactSNTable

    @number_of_rows_in_the_contact_sn_table.setter
    def number_of_rows_in_the_contact_sn_table(self, value: 'int'):
        self.wrapped.NumberOfRowsInTheContactSNTable = int(value) if value else 0

    @property
    def material(self) -> '_604.PlasticCylindricalGearMaterial':
        '''PlasticCylindricalGearMaterial: 'Material' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_604.PlasticCylindricalGearMaterial)(self.wrapped.Material) if self.wrapped.Material else None

    @property
    def bending_stress_cycle_data(self) -> 'List[_270.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]':
        '''List[StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]: 'BendingStressCycleData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BendingStressCycleData, constructor.new(_270.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial))
        return value

    @property
    def contact_stress_cycle_data(self) -> 'List[_271.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]':
        '''List[StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]: 'ContactStressCycleData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ContactStressCycleData, constructor.new(_271.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial))
        return value

    @property
    def bending_stress_cycle_data_for_damage_tables(self) -> 'List[_270.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]':
        '''List[StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial]: 'BendingStressCycleDataForDamageTables' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BendingStressCycleDataForDamageTables, constructor.new(_270.StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial))
        return value

    @property
    def contact_stress_cycle_data_for_damage_tables(self) -> 'List[_271.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]':
        '''List[StressCyclesDataForTheContactSNCurveOfAPlasticMaterial]: 'ContactStressCycleDataForDamageTables' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ContactStressCycleDataForDamageTables, constructor.new(_271.StressCyclesDataForTheContactSNCurveOfAPlasticMaterial))
        return value
