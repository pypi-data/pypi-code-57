'''_6203.py

GearMeshTEExcitationDetail
'''


from mastapy.system_model.analyses_and_results.static_loads import _6220
from mastapy._internal import conversion, constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _6189, _6180
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_TE_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'GearMeshTEExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshTEExcitationDetail',)


class GearMeshTEExcitationDetail(_6180.AbstractPeriodicExcitationDetail):
    '''GearMeshTEExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_TE_EXCITATION_DETAIL
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshTEExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)

    def get_compliance_and_force_data(self, excitation_type: '_6220.TEExcitationType') -> '_6189.ComplianceAndForceData':
        ''' 'GetComplianceAndForceData' is the original name of this method.

        Args:
            excitation_type (mastapy.system_model.analyses_and_results.static_loads.TEExcitationType)

        Returns:
            mastapy.system_model.analyses_and_results.gear_whine_analyses.ComplianceAndForceData
        '''

        excitation_type = conversion.mp_to_pn_enum(excitation_type)
        method_result = self.wrapped.GetComplianceAndForceData(excitation_type)
        return constructor.new(_6189.ComplianceAndForceData)(method_result) if method_result else None
