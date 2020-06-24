'''_4077.py

KlingelnbergCycloPalloidConicalGearParametricStudyTool
'''


from mastapy.system_model.part_model.gears import _2000, _2012, _2013
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4068
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'KlingelnbergCycloPalloidConicalGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearParametricStudyTool',)


class KlingelnbergCycloPalloidConicalGearParametricStudyTool(_4068.ConicalGearParametricStudyTool):
    '''KlingelnbergCycloPalloidConicalGearParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_PARAMETRIC_STUDY_TOOL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2000.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2000.KlingelnbergCycloPalloidConicalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2012.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGear':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2012.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2013.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGear':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2013.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
