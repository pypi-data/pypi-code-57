'''_5414.py

BearingSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6054
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5442
from mastapy._internal.python_net import python_net_import

_BEARING_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'BearingSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingSingleMeshWhineAnalysis',)


class BearingSingleMeshWhineAnalysis(_5442.ConnectorSingleMeshWhineAnalysis):
    '''BearingSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1985.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6054.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6054.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[BearingSingleMeshWhineAnalysis]':
        '''List[BearingSingleMeshWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingSingleMeshWhineAnalysis))
        return value
