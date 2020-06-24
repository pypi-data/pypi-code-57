'''_5364.py

PlanetaryGearSetCompoundModalAnalysesAtSpeeds
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5332
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'PlanetaryGearSetCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetCompoundModalAnalysesAtSpeeds',)


class PlanetaryGearSetCompoundModalAnalysesAtSpeeds(_5332.CylindricalGearSetCompoundModalAnalysesAtSpeeds):
    '''PlanetaryGearSetCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
