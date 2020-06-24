'''_5142.py

ConicalGearMeshCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5163
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'ConicalGearMeshCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMeshCompoundMultiBodyDynamicsAnalysis',)


class ConicalGearMeshCompoundMultiBodyDynamicsAnalysis(_5163.GearMeshCompoundMultiBodyDynamicsAnalysis):
    '''ConicalGearMeshCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MESH_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMeshCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def planetaries(self) -> 'List[ConicalGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[ConicalGearMeshCompoundMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ConicalGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value
