'''_6213.py

ExcitationSourceSelection
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.whine_analyses_results import _6216, _6214
from mastapy._internal.python_net import python_net_import

_EXCITATION_SOURCE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.WhineAnalysesResults', 'ExcitationSourceSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ExcitationSourceSelection',)


class ExcitationSourceSelection(_6214.ExcitationSourceSelectionBase):
    '''ExcitationSourceSelection

    This is a mastapy class.
    '''

    TYPE = _EXCITATION_SOURCE_SELECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExcitationSourceSelection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def invert_selection(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'InvertSelection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InvertSelection

    @property
    def harmonic_selections(self) -> 'List[_6216.HarmonicSelection]':
        '''List[HarmonicSelection]: 'HarmonicSelections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HarmonicSelections, constructor.new(_6216.HarmonicSelection))
        return value
