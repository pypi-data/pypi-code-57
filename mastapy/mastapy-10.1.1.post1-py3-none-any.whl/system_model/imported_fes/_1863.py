'''_1863.py

ImportedFeLinkWithSelection
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.system_model.imported_fes import (
    _1833, _1866, _1860, _1864,
    _1870, _1894, _1862, _1867,
    _1869, _1861, _1893
)
from mastapy._internal.cast_exception import CastException
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_LINK_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFeLinkWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFeLinkWithSelection',)


class ImportedFeLinkWithSelection(_1.APIBase):
    '''ImportedFeLinkWithSelection

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_LINK_WITH_SELECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFeLinkWithSelection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def add_selected_nodes(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddSelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddSelectedNodes

    @property
    def delete_all_nodes(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'DeleteAllNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DeleteAllNodes

    @property
    def select_component(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SelectComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SelectComponent

    @property
    def link(self) -> '_1833.ImportedFELink':
        '''ImportedFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1833.ImportedFELink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_node_link(self) -> '_1866.ImportedFENodeLink':
        '''ImportedFENodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Link.__class__.__qualname__ != 'ImportedFENodeLink':
            raise CastException('Failed to cast link to ImportedFENodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1866.ImportedFENodeLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_electric_machine_stator_link(self) -> '_1860.ImportedFEElectricMachineStatorLink':
        '''ImportedFEElectricMachineStatorLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Link.__class__.__qualname__ != 'ImportedFEElectricMachineStatorLink':
            raise CastException('Failed to cast link to ImportedFEElectricMachineStatorLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1860.ImportedFEElectricMachineStatorLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_multi_node_connector_link(self) -> '_1864.ImportedFEMultiNodeConnectorLink':
        '''ImportedFEMultiNodeConnectorLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Link.__class__.__qualname__ != 'ImportedFEMultiNodeConnectorLink':
            raise CastException('Failed to cast link to ImportedFEMultiNodeConnectorLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1864.ImportedFEMultiNodeConnectorLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_point_load_link(self) -> '_1870.ImportedFEPointLoadLink':
        '''ImportedFEPointLoadLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Link.__class__.__qualname__ != 'ImportedFEPointLoadLink':
            raise CastException('Failed to cast link to ImportedFEPointLoadLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1870.ImportedFEPointLoadLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_shaft_hub_connection_fe_link(self) -> '_1894.ShaftHubConnectionFELink':
        '''ShaftHubConnectionFELink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Link.__class__.__qualname__ != 'ShaftHubConnectionFELink':
            raise CastException('Failed to cast link to ShaftHubConnectionFELink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1894.ShaftHubConnectionFELink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_gear_with_duplicated_meshes_link(self) -> '_1862.ImportedFEGearWithDuplicatedMeshesLink':
        '''ImportedFEGearWithDuplicatedMeshesLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Link.__class__.__qualname__ != 'ImportedFEGearWithDuplicatedMeshesLink':
            raise CastException('Failed to cast link to ImportedFEGearWithDuplicatedMeshesLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1862.ImportedFEGearWithDuplicatedMeshesLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planetary_connector_multi_node_link(self) -> '_1867.ImportedFEPlanetaryConnectorMultiNodeLink':
        '''ImportedFEPlanetaryConnectorMultiNodeLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Link.__class__.__qualname__ != 'ImportedFEPlanetaryConnectorMultiNodeLink':
            raise CastException('Failed to cast link to ImportedFEPlanetaryConnectorMultiNodeLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1867.ImportedFEPlanetaryConnectorMultiNodeLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_planet_carrier_link(self) -> '_1869.ImportedFEPlanetCarrierLink':
        '''ImportedFEPlanetCarrierLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Link.__class__.__qualname__ != 'ImportedFEPlanetCarrierLink':
            raise CastException('Failed to cast link to ImportedFEPlanetCarrierLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1869.ImportedFEPlanetCarrierLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_imported_fe_gear_mesh_link(self) -> '_1861.ImportedFEGearMeshLink':
        '''ImportedFEGearMeshLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Link.__class__.__qualname__ != 'ImportedFEGearMeshLink':
            raise CastException('Failed to cast link to ImportedFEGearMeshLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1861.ImportedFEGearMeshLink)(self.wrapped.Link) if self.wrapped.Link else None

    @property
    def link_of_type_rolling_ring_connection_link(self) -> '_1893.RollingRingConnectionLink':
        '''RollingRingConnectionLink: 'Link' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Link.__class__.__qualname__ != 'RollingRingConnectionLink':
            raise CastException('Failed to cast link to RollingRingConnectionLink. Expected: {}.'.format(self.wrapped.Link.__class__.__qualname__))

        return constructor.new(_1893.RollingRingConnectionLink)(self.wrapped.Link) if self.wrapped.Link else None
