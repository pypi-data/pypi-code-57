'''_5122.py

PlanetaryGearSetCompoundModalAnalysesAtStiffnesses
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _5090
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'PlanetaryGearSetCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetCompoundModalAnalysesAtStiffnesses',)


class PlanetaryGearSetCompoundModalAnalysesAtStiffnesses(_5090.CylindricalGearSetCompoundModalAnalysesAtStiffnesses):
    '''PlanetaryGearSetCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
