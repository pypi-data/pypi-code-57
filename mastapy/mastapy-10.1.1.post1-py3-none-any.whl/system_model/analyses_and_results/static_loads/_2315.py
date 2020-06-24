'''_2315.py

BevelDifferentialGearLoadCase
'''


from mastapy.system_model.part_model.gears import _2003
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2319
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BevelDifferentialGearLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearLoadCase',)


class BevelDifferentialGearLoadCase(_2319.BevelGearLoadCase):
    '''BevelDifferentialGearLoadCase

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_LOAD_CASE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2003.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2003.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
