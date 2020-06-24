'''_3746.py

CVTGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _1987
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2181
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3739
from mastapy._internal.python_net import python_net_import

_CVT_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'CVTGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTGearWhineAnalysis',)


class CVTGearWhineAnalysis(_3739.BeltDriveGearWhineAnalysis):
    '''CVTGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1987.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def system_deflection_results(self) -> '_2181.CVTSystemDeflection':
        '''CVTSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.CVTSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
