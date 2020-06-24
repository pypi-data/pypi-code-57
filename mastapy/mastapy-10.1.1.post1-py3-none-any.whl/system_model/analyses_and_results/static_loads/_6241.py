'''_6241.py

UnbalancedMassHarmonicLoadData
'''


from typing import List

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.math_utility import _1218, _1006
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6288
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_HARMONIC_LOAD_DATA = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'UnbalancedMassHarmonicLoadData')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassHarmonicLoadData',)


class UnbalancedMassHarmonicLoadData(_6288.SpeedDependentHarmonicLoadData):
    '''UnbalancedMassHarmonicLoadData

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_HARMONIC_LOAD_DATA
    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassHarmonicLoadData.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def degree_of_freedom(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom':
        '''enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom: 'DegreeOfFreedom' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom)(self.wrapped.DegreeOfFreedom) if self.wrapped.DegreeOfFreedom else None

    @degree_of_freedom.setter
    def degree_of_freedom(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DegreesOfFreedom.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DegreeOfFreedom = value

    @property
    def excitations(self) -> 'List[_1006.FourierSeries]':
        '''List[FourierSeries]: 'Excitations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Excitations, constructor.new(_1006.FourierSeries))
        return value
