'''_2159.py

ConcentricPartGroupCombinationSystemDeflectionResults
'''


from typing import List

from mastapy.scripting import _712
from mastapy._internal import constructor, conversion
from mastapy.system_model.drawing import _1753
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CONCENTRIC_PART_GROUP_COMBINATION_SYSTEM_DEFLECTION_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConcentricPartGroupCombinationSystemDeflectionResults')


__docformat__ = 'restructuredtext en'
__all__ = ('ConcentricPartGroupCombinationSystemDeflectionResults',)


class ConcentricPartGroupCombinationSystemDeflectionResults(_1.APIBase):
    '''ConcentricPartGroupCombinationSystemDeflectionResults

    This is a mastapy class.
    '''

    TYPE = _CONCENTRIC_PART_GROUP_COMBINATION_SYSTEM_DEFLECTION_RESULTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConcentricPartGroupCombinationSystemDeflectionResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def twod_drawing(self) -> '_712.SMTBitmap':
        '''SMTBitmap: 'TwoDDrawing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_712.SMTBitmap)(self.wrapped.TwoDDrawing) if self.wrapped.TwoDDrawing else None

    @property
    def shaft_deflections_in_view_coordinate_system(self) -> 'List[_1753.ConcentricPartGroupCombinationSystemDeflectionShaftResults]':
        '''List[ConcentricPartGroupCombinationSystemDeflectionShaftResults]: 'ShaftDeflectionsInViewCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftDeflectionsInViewCoordinateSystem, constructor.new(_1753.ConcentricPartGroupCombinationSystemDeflectionShaftResults))
        return value
