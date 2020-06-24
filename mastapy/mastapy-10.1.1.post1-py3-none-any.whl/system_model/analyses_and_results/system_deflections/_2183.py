'''_2183.py

CVTPulleySystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2023
from mastapy._internal import constructor, conversion
from mastapy.math_utility.measured_vectors import _1250
from mastapy.system_model.analyses_and_results.system_deflections import _2185
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'CVTPulleySystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleySystemDeflection',)


class CVTPulleySystemDeflection(_2185.PulleySystemDeflection):
    '''CVTPulleySystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleySystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2023.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2023.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def fixed_sheave_contact_results(self) -> 'List[_1250.NodeResults]':
        '''List[NodeResults]: 'FixedSheaveContactResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FixedSheaveContactResults, constructor.new(_1250.NodeResults))
        return value

    @property
    def moving_sheave_contact_results(self) -> 'List[_1250.NodeResults]':
        '''List[NodeResults]: 'MovingSheaveContactResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MovingSheaveContactResults, constructor.new(_1250.NodeResults))
        return value
