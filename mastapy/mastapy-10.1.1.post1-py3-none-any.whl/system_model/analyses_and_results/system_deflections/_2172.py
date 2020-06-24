'''_2172.py

ConnectorSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1915, _1908, _1929
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.couplings import _2028
from mastapy.system_model.analyses_and_results.system_deflections import _2203, _2218
from mastapy.math_utility.measured_vectors import _1253
from mastapy.utility.units_and_measurements.measurements import _1303, _1367
from mastapy.system_model.imported_fes import _1871
from mastapy._internal.python_net import python_net_import

_CONNECTOR_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConnectorSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorSystemDeflection',)


class ConnectorSystemDeflection(_2218.MountableComponentSystemDeflection):
    '''ConnectorSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectorSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def convergence_delta_energy(self) -> 'float':
        '''float: 'ConvergenceDeltaEnergy' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConvergenceDeltaEnergy

    @property
    def component_design(self) -> '_1915.Connector':
        '''Connector: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1915.Connector)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bearing(self) -> '_1908.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Bearing':
            raise CastException('Failed to cast component_design to Bearing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1908.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_oil_seal(self) -> '_1929.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'OilSeal':
            raise CastException('Failed to cast component_design to OilSeal. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1929.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft_hub_connection(self) -> '_2028.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ShaftHubConnection':
            raise CastException('Failed to cast component_design to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2028.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def outer_imported_fe(self) -> '_2203.ImportedFEComponentSystemDeflection':
        '''ImportedFEComponentSystemDeflection: 'OuterImportedFE' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2203.ImportedFEComponentSystemDeflection)(self.wrapped.OuterImportedFE) if self.wrapped.OuterImportedFE else None

    @property
    def force_on_outer_support_in_wcs(self) -> '_1253.VectorWithLinearAndAngularComponents[_1303.Force, _1367.Torque]':
        '''VectorWithLinearAndAngularComponents[Force, Torque]: 'ForceOnOuterSupportInWCS' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1253.VectorWithLinearAndAngularComponents)[_1303.Force, _1367.Torque](self.wrapped.ForceOnOuterSupportInWCS) if self.wrapped.ForceOnOuterSupportInWCS else None

    @property
    def force_on_outer_support_in_lcs(self) -> '_1253.VectorWithLinearAndAngularComponents[_1303.Force, _1367.Torque]':
        '''VectorWithLinearAndAngularComponents[Force, Torque]: 'ForceOnOuterSupportInLCS' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1253.VectorWithLinearAndAngularComponents)[_1303.Force, _1367.Torque](self.wrapped.ForceOnOuterSupportInLCS) if self.wrapped.ForceOnOuterSupportInLCS else None

    @property
    def outer_imported_fe_nodes(self) -> 'List[_1871.ImportedFEStiffnessNode]':
        '''List[ImportedFEStiffnessNode]: 'OuterImportedFENodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OuterImportedFENodes, constructor.new(_1871.ImportedFEStiffnessNode))
        return value
