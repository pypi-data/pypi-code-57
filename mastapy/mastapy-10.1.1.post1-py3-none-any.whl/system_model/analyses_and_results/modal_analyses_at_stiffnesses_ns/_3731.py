'''_3731.py

BevelDifferentialGearModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.gears import _2054
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6057
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3736
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'BevelDifferentialGearModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearModalAnalysesAtStiffnesses',)


class BevelDifferentialGearModalAnalysesAtStiffnesses(_3736.BevelGearModalAnalysesAtStiffnesses):
    '''BevelDifferentialGearModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2054.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2054.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6057.BevelDifferentialGearLoadCase':
        '''BevelDifferentialGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6057.BevelDifferentialGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
