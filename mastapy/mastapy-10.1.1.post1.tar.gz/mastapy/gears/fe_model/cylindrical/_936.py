'''_936.py

CylindricalGearMeshFEModel
'''


from typing import List

from mastapy.gears.fe_model import _931, _932
from mastapy.gears import _128
from mastapy._internal import conversion, constructor
from mastapy.gears.ltca import _613
from mastapy import _6501
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_FE_MODEL = python_net_import('SMT.MastaAPI.Gears.FEModel.Cylindrical', 'CylindricalGearMeshFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshFEModel',)


class CylindricalGearMeshFEModel(_932.GearMeshFEModel):
    '''CylindricalGearMeshFEModel

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_FE_MODEL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshFEModel.TYPE'):
        super().__init__(instance_to_wrap)

    def stiffness_wrt_contacts_for(self, gear: '_931.GearFEModel', flank: '_128.GearFlanks') -> 'List[_613.GearContactStiffness]':
        ''' 'StiffnessWrtContactsFor' is the original name of this method.

        Args:
            gear (mastapy.gears.fe_model.GearFEModel)
            flank (mastapy.gears.GearFlanks)

        Returns:
            List[mastapy.gears.ltca.GearContactStiffness]
        '''

        flank = conversion.mp_to_pn_enum(flank)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.StiffnessWrtContactsFor(gear.wrapped if gear else None, flank), constructor.new(_613.GearContactStiffness))

    def stiffness_wrt_contacts_for_with_progress(self, gear: '_931.GearFEModel', flank: '_128.GearFlanks', progress: '_6501.TaskProgress') -> 'List[_613.GearContactStiffness]':
        ''' 'StiffnessWrtContactsFor' is the original name of this method.

        Args:
            gear (mastapy.gears.fe_model.GearFEModel)
            flank (mastapy.gears.GearFlanks)
            progress (mastapy.TaskProgress)

        Returns:
            List[mastapy.gears.ltca.GearContactStiffness]
        '''

        flank = conversion.mp_to_pn_enum(flank)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.StiffnessWrtContactsFor(gear.wrapped if gear else None, flank, progress.wrapped if progress else None), constructor.new(_613.GearContactStiffness))
