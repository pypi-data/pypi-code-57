'''_2383.py

SystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2385
from mastapy.system_model.imported_fes import _1890
from mastapy.system_model.analyses_and_results.analysis_cases import _3379
from mastapy._internal.python_net import python_net_import

_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemDeflection',)


class SystemDeflection(_3379.FEAnalysis):
    '''SystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def current_time(self) -> 'float':
        '''float: 'CurrentTime' is the original name of this property.'''

        return self.wrapped.CurrentTime

    @current_time.setter
    def current_time(self, value: 'float'):
        self.wrapped.CurrentTime = float(value) if value else 0.0

    @property
    def include_twist_in_misalignments(self) -> 'bool':
        '''bool: 'IncludeTwistInMisalignments' is the original name of this property.'''

        return self.wrapped.IncludeTwistInMisalignments

    @include_twist_in_misalignments.setter
    def include_twist_in_misalignments(self, value: 'bool'):
        self.wrapped.IncludeTwistInMisalignments = bool(value) if value else False

    @property
    def iterations(self) -> 'int':
        '''int: 'Iterations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Iterations

    @property
    def maximum_circulating_power(self) -> 'float':
        '''float: 'MaximumCirculatingPower' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumCirculatingPower

    @property
    def energy_lost(self) -> 'float':
        '''float: 'EnergyLost' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EnergyLost

    @property
    def energy_input(self) -> 'float':
        '''float: 'EnergyInput' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EnergyInput

    @property
    def energy_output(self) -> 'float':
        '''float: 'EnergyOutput' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EnergyOutput

    @property
    def power_lost(self) -> 'float':
        '''float: 'PowerLost' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PowerLost

    @property
    def total_system_efficiency(self) -> 'float':
        '''float: 'TotalSystemEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalSystemEfficiency

    @property
    def power_error(self) -> 'float':
        '''float: 'PowerError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PowerError

    @property
    def power_convergence_error(self) -> 'float':
        '''float: 'PowerConvergenceError' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PowerConvergenceError

    @property
    def total_input_power(self) -> 'float':
        '''float: 'TotalInputPower' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalInputPower

    @property
    def largest_power_across_a_connection(self) -> 'float':
        '''float: 'LargestPowerAcrossAConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LargestPowerAcrossAConnection

    @property
    def analysis_options(self) -> '_2385.SystemDeflectionOptions':
        '''SystemDeflectionOptions: 'AnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2385.SystemDeflectionOptions)(self.wrapped.AnalysisOptions) if self.wrapped.AnalysisOptions else None

    @property
    def bearing_race_fes(self) -> 'List[_1890.RaceBearingFESystemDeflection]':
        '''List[RaceBearingFESystemDeflection]: 'BearingRaceFEs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BearingRaceFEs, constructor.new(_1890.RaceBearingFESystemDeflection))
        return value
