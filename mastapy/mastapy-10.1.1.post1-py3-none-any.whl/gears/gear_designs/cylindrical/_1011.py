'''_1011.py

TiffAnalysisSettings
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _967
from mastapy.utility import _334
from mastapy._internal.python_net import python_net_import

_TIFF_ANALYSIS_SETTINGS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'TiffAnalysisSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('TiffAnalysisSettings',)


class TiffAnalysisSettings(_334.IndependentReportablePropertiesBase['TiffAnalysisSettings']):
    '''TiffAnalysisSettings

    This is a mastapy class.
    '''

    TYPE = _TIFF_ANALYSIS_SETTINGS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'TiffAnalysisSettings.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_rotations_for_findley(self) -> 'int':
        '''int: 'NumberOfRotationsForFindley' is the original name of this property.'''

        return self.wrapped.NumberOfRotationsForFindley

    @number_of_rotations_for_findley.setter
    def number_of_rotations_for_findley(self, value: 'int'):
        self.wrapped.NumberOfRotationsForFindley = int(value) if value else 0

    @property
    def case_hardening_properties_for_fe_analysis(self) -> '_967.CaseHardeningPropertiesForFEAnalysis':
        '''CaseHardeningPropertiesForFEAnalysis: 'CaseHardeningPropertiesForFEAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_967.CaseHardeningPropertiesForFEAnalysis)(self.wrapped.CaseHardeningPropertiesForFEAnalysis) if self.wrapped.CaseHardeningPropertiesForFEAnalysis else None
