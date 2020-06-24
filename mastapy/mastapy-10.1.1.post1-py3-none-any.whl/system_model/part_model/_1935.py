'''_1935.py

RootAssembly
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model import _1719
from mastapy.geometry import _283
from mastapy.system_model.part_model.projections import _1945
from mastapy.system_model.part_model.part_groups import _1950
from mastapy.system_model.part_model import _1904
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssembly',)


class RootAssembly(_1904.Assembly):
    '''RootAssembly

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssembly.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def attempt_to_fix_all_gear_sets(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AttemptToFixAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AttemptToFixAllGearSets

    @property
    def attempt_to_fix_all_cylindrical_gear_sets_by_changing_normal_module(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AttemptToFixAllCylindricalGearSetsByChangingNormalModule' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AttemptToFixAllCylindricalGearSetsByChangingNormalModule

    @property
    def open_imported_fe_version_comparer(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'OpenImportedFEVersionComparer' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OpenImportedFEVersionComparer

    @property
    def model(self) -> '_1719.Design':
        '''Design: 'Model' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1719.Design)(self.wrapped.Model) if self.wrapped.Model else None

    @property
    def packaging_limits(self) -> '_283.PackagingLimits':
        '''PackagingLimits: 'PackagingLimits' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_283.PackagingLimits)(self.wrapped.PackagingLimits) if self.wrapped.PackagingLimits else None

    @property
    def parallel_part_groups_drawing_order(self) -> 'List[_1945.SpecifiedParallelPartGroupDrawingOrder]':
        '''List[SpecifiedParallelPartGroupDrawingOrder]: 'ParallelPartGroupsDrawingOrder' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ParallelPartGroupsDrawingOrder, constructor.new(_1945.SpecifiedParallelPartGroupDrawingOrder))
        return value

    @property
    def parallel_part_groups(self) -> 'List[_1950.ParallelPartGroup]':
        '''List[ParallelPartGroup]: 'ParallelPartGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ParallelPartGroups, constructor.new(_1950.ParallelPartGroup))
        return value
