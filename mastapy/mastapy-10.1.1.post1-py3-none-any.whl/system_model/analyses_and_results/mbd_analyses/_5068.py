'''_5068.py

ShaftMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2022
from mastapy.system_model.analyses_and_results.static_loads import _6174
from mastapy.system_model.analyses_and_results.mbd_analyses import _4967
from mastapy._internal.python_net import python_net_import

_SHAFT_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ShaftMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftMultiBodyDynamicsAnalysis',)


class ShaftMultiBodyDynamicsAnalysis(_4967.AbstractShaftOrHousingMultiBodyDynamicsAnalysis):
    '''ShaftMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def elastic_radial_deflections(self) -> 'List[float]':
        '''List[float]: 'ElasticRadialDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticRadialDeflections)
        return value

    @property
    def elastic_local_x_deflections(self) -> 'List[float]':
        '''List[float]: 'ElasticLocalXDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticLocalXDeflections)
        return value

    @property
    def elastic_local_y_deflections(self) -> 'List[float]':
        '''List[float]: 'ElasticLocalYDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticLocalYDeflections)
        return value

    @property
    def elastic_local_z_deflections(self) -> 'List[float]':
        '''List[float]: 'ElasticLocalZDeflections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticLocalZDeflections)
        return value

    @property
    def angular_velocities(self) -> 'List[float]':
        '''List[float]: 'AngularVelocities' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.AngularVelocities)
        return value

    @property
    def elastic_twists(self) -> 'List[float]':
        '''List[float]: 'ElasticTwists' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElasticTwists)
        return value

    @property
    def component_design(self) -> '_2022.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2022.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6174.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6174.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftMultiBodyDynamicsAnalysis]':
        '''List[ShaftMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftMultiBodyDynamicsAnalysis))
        return value
