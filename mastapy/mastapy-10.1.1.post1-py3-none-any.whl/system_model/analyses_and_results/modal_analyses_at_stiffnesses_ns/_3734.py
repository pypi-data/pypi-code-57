'''_3734.py

BevelDifferentialSunGearModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.gears import _2057
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3731
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'BevelDifferentialSunGearModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearModalAnalysesAtStiffnesses',)


class BevelDifferentialSunGearModalAnalysesAtStiffnesses(_3731.BevelDifferentialGearModalAnalysesAtStiffnesses):
    '''BevelDifferentialSunGearModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2057.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2057.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
