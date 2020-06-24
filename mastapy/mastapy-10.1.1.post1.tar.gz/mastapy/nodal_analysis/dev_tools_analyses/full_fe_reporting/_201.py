'''_201.py

ElementPropertiesBeam
'''


from mastapy.fe_tools.vis_tools_global.vis_tools_global_enums import _216
from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _208
from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_BEAM = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ElementPropertiesBeam')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesBeam',)


class ElementPropertiesBeam(_208.ElementPropertiesWithMaterial):
    '''ElementPropertiesBeam

    This is a mastapy class.
    '''

    TYPE = _ELEMENT_PROPERTIES_BEAM
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElementPropertiesBeam.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def section_type(self) -> '_216.BeamSectionType':
        '''BeamSectionType: 'SectionType' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.SectionType)
        return constructor.new(_216.BeamSectionType)(value) if value else None

    @property
    def section_dimensions(self) -> 'str':
        '''str: 'SectionDimensions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SectionDimensions
