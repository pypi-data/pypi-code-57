'''_6105.py

ElectricMachineHarmonicLoadDataFromJMAG
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6107, _6110
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_JMAG = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineHarmonicLoadDataFromJMAG')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineHarmonicLoadDataFromJMAG',)


class ElectricMachineHarmonicLoadDataFromJMAG(_6107.ElectricMachineHarmonicLoadDataFromMotorPackages['_6110.ElectricMachineHarmonicLoadJMAGImportOptions']):
    '''ElectricMachineHarmonicLoadDataFromJMAG

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_JMAG

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineHarmonicLoadDataFromJMAG.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def use_stator_radius_from_masta_model(self) -> 'bool':
        '''bool: 'UseStatorRadiusFromMASTAModel' is the original name of this property.'''

        return self.wrapped.UseStatorRadiusFromMASTAModel

    @use_stator_radius_from_masta_model.setter
    def use_stator_radius_from_masta_model(self, value: 'bool'):
        self.wrapped.UseStatorRadiusFromMASTAModel = bool(value) if value else False
