'''_196.py

ContactPairReporting
'''


from typing import Callable

from mastapy._internal import constructor, conversion
from mastapy.fe_tools.vis_tools_global.vis_tools_global_enums import _235, _236
from mastapy._internal.implicit import overridable
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CONTACT_PAIR_REPORTING = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ContactPairReporting')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactPairReporting',)


class ContactPairReporting(_1.APIBase):
    '''ContactPairReporting

    This is a mastapy class.
    '''

    TYPE = _CONTACT_PAIR_REPORTING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ContactPairReporting.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def id(self) -> 'int':
        '''int: 'ID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ID

    @property
    def master_type(self) -> '_235.ContactPairMasterType':
        '''ContactPairMasterType: 'MasterType' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.MasterType)
        return constructor.new(_235.ContactPairMasterType)(value) if value else None

    @property
    def slave_type(self) -> '_236.ContactPairSlaveType':
        '''ContactPairSlaveType: 'SlaveType' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.SlaveType)
        return constructor.new(_236.ContactPairSlaveType)(value) if value else None

    @property
    def property_id(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'PropertyID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_int)(self.wrapped.PropertyID) if self.wrapped.PropertyID else None

    @property
    def adjust_distance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AdjustDistance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AdjustDistance) if self.wrapped.AdjustDistance else None

    @adjust_distance.setter
    def adjust_distance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AdjustDistance = value

    @property
    def position_tolerance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PositionTolerance' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PositionTolerance) if self.wrapped.PositionTolerance else None

    @position_tolerance.setter
    def position_tolerance(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.PositionTolerance = value

    @property
    def swap_master_and_slave_surfaces(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SwapMasterAndSlaveSurfaces' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SwapMasterAndSlaveSurfaces
