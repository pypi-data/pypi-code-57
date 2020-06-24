'''_1929.py

OilSeal
'''


from mastapy.system_model.part_model import _1930, _1915
from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results import _1533
from mastapy._internal.python_net import python_net_import

_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSeal',)


class OilSeal(_1915.Connector):
    '''OilSeal

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSeal.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def oil_seal_material(self) -> '_1930.OilSealMaterialType':
        '''OilSealMaterialType: 'OilSealMaterial' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OilSealMaterial)
        return constructor.new(_1930.OilSealMaterialType)(value) if value else None

    @oil_seal_material.setter
    def oil_seal_material(self, value: '_1930.OilSealMaterialType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OilSealMaterial = value

    @property
    def oil_seal_characteristic_life(self) -> 'float':
        '''float: 'OilSealCharacteristicLife' is the original name of this property.'''

        return self.wrapped.OilSealCharacteristicLife

    @oil_seal_characteristic_life.setter
    def oil_seal_characteristic_life(self, value: 'float'):
        self.wrapped.OilSealCharacteristicLife = float(value) if value else 0.0

    @property
    def oil_seal_mean_time_before_failure(self) -> 'float':
        '''float: 'OilSealMeanTimeBeforeFailure' is the original name of this property.'''

        return self.wrapped.OilSealMeanTimeBeforeFailure

    @oil_seal_mean_time_before_failure.setter
    def oil_seal_mean_time_before_failure(self, value: 'float'):
        self.wrapped.OilSealMeanTimeBeforeFailure = float(value) if value else 0.0

    @property
    def oil_seal_frictional_torque_coefficient(self) -> 'float':
        '''float: 'OilSealFrictionalTorqueCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OilSealFrictionalTorqueCoefficient

    @property
    def oil_seal_orientation(self) -> '_1533.Orientations':
        '''Orientations: 'OilSealOrientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.OilSealOrientation)
        return constructor.new(_1533.Orientations)(value) if value else None

    @oil_seal_orientation.setter
    def oil_seal_orientation(self, value: '_1533.Orientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.OilSealOrientation = value
