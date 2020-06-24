'''_6266.py

ElectricMachineHarmonicLoadDataFromMotorCAD
'''


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6267, _6271
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_MOTOR_CAD = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineHarmonicLoadDataFromMotorCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineHarmonicLoadDataFromMotorCAD',)


class ElectricMachineHarmonicLoadDataFromMotorCAD(_6267.ElectricMachineHarmonicLoadDataFromMotorPackages['_6271.ElectricMachineHarmonicLoadMotorCADImportOptions']):
    '''ElectricMachineHarmonicLoadDataFromMotorCAD

    This is a mastapy class.
    '''

    TYPE = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_MOTOR_CAD
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineHarmonicLoadDataFromMotorCAD.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def use_stator_radius_from_masta_model(self) -> 'bool':
        '''bool: 'UseStatorRadiusFromMASTAModel' is the original name of this property.'''

        return self.wrapped.UseStatorRadiusFromMASTAModel

    @use_stator_radius_from_masta_model.setter
    def use_stator_radius_from_masta_model(self, value: 'bool'):
        self.wrapped.UseStatorRadiusFromMASTAModel = bool(value) if value else False
