'''_1808.py

KlingelnbergCycloPalloidHypoidGearMesh
'''


from mastapy.gears.gear_designs.klingelnberg_hypoid import _438
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import _1807
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidHypoidGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearMesh',)


class KlingelnbergCycloPalloidHypoidGearMesh(_1807.KlingelnbergCycloPalloidConicalGearMesh):
    '''KlingelnbergCycloPalloidHypoidGearMesh

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH
    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearMesh.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(self) -> '_438.KlingelnbergCycloPalloidHypoidGearMeshDesign':
        '''KlingelnbergCycloPalloidHypoidGearMeshDesign: 'KlingelnbergCycloPalloidHypoidGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_438.KlingelnbergCycloPalloidHypoidGearMeshDesign)(self.wrapped.KlingelnbergCycloPalloidHypoidGearMeshDesign) if self.wrapped.KlingelnbergCycloPalloidHypoidGearMeshDesign else None
