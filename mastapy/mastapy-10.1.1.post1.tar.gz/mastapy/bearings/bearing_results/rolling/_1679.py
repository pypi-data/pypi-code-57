'''_1679.py

RaceFittingThermalResults
'''


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RACE_FITTING_THERMAL_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'RaceFittingThermalResults')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceFittingThermalResults',)


class RaceFittingThermalResults(_0.APIBase):
    '''RaceFittingThermalResults

    This is a mastapy class.
    '''

    TYPE = _RACE_FITTING_THERMAL_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RaceFittingThermalResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def interfacial_interference(self) -> 'float':
        '''float: 'InterfacialInterference' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InterfacialInterference

    @property
    def interfacial_normal_stress(self) -> 'float':
        '''float: 'InterfacialNormalStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InterfacialNormalStress

    @property
    def change_in_diameter_due_to_press_fitting(self) -> 'float':
        '''float: 'ChangeInDiameterDueToPressFitting' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ChangeInDiameterDueToPressFitting

    @property
    def interfacial_clearance_included_in_analysis(self) -> 'bool':
        '''bool: 'InterfacialClearanceIncludedInAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InterfacialClearanceIncludedInAnalysis
