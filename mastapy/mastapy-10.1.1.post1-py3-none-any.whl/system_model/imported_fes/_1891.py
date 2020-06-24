'''_1891.py

RaceBearingFEWithSelection
'''


from mastapy.math_utility import _1216
from mastapy._internal import constructor
from mastapy.system_model.imported_fes import _1889, _1839
from mastapy._internal.python_net import python_net_import

_RACE_BEARING_FE_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'RaceBearingFEWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceBearingFEWithSelection',)


class RaceBearingFEWithSelection(_1839.BaseFEWithSelection):
    '''RaceBearingFEWithSelection

    This is a mastapy class.
    '''

    TYPE = _RACE_BEARING_FE_WITH_SELECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RaceBearingFEWithSelection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def manual_alignment(self) -> '_1216.CoordinateSystemEditor':
        '''CoordinateSystemEditor: 'ManualAlignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1216.CoordinateSystemEditor)(self.wrapped.ManualAlignment) if self.wrapped.ManualAlignment else None

    @property
    def race_bearing(self) -> '_1889.RaceBearingFE':
        '''RaceBearingFE: 'RaceBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1889.RaceBearingFE)(self.wrapped.RaceBearing) if self.wrapped.RaceBearing else None
