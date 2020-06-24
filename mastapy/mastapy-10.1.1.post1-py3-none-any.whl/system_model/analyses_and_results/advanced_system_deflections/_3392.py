'''_3392.py

CVTAdvancedSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _1987
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3385
from mastapy._internal.python_net import python_net_import

_CVT_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CVTAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTAdvancedSystemDeflection',)


class CVTAdvancedSystemDeflection(_3385.BeltDriveAdvancedSystemDeflection):
    '''CVTAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CVT_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1987.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
