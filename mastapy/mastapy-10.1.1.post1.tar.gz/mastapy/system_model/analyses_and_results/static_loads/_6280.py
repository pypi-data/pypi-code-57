'''_6280.py

HarmonicLoadDataJMAGImport
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6262, _6279, _6270
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_JMAG_IMPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataJMAGImport')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataJMAGImport',)


class HarmonicLoadDataJMAGImport(_6279.HarmonicLoadDataImportFromMotorPackages['_6270.ElectricMachineHarmonicLoadJMAGImportOptions']):
    '''HarmonicLoadDataJMAGImport

    This is a mastapy class.
    '''

    TYPE = _HARMONIC_LOAD_DATA_JMAG_IMPORT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataJMAGImport.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def select_jmag_file(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectJMAGFile' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectJMAGFile

    @property
    def electric_machine_data_per_speed(self) -> 'List[_6262.DataFromJMAGPerSpeed]':
        '''List[DataFromJMAGPerSpeed]: 'ElectricMachineDataPerSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ElectricMachineDataPerSpeed, constructor.new(_6262.DataFromJMAGPerSpeed))
        return value
