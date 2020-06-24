'''_2015.py

RootAssembly
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model import _1792
from mastapy.geometry import _113
from mastapy.system_model.part_model.projections import _2025
from mastapy.system_model.part_model.part_groups import _2030
from mastapy.system_model.part_model import _1980
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssembly',)


class RootAssembly(_1980.Assembly):
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
    def model(self) -> '_1792.Design':
        '''Design: 'Model' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1792.Design)(self.wrapped.Model) if self.wrapped.Model else None

    @property
    def packaging_limits(self) -> '_113.PackagingLimits':
        '''PackagingLimits: 'PackagingLimits' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_113.PackagingLimits)(self.wrapped.PackagingLimits) if self.wrapped.PackagingLimits else None

    @property
    def parallel_part_groups_drawing_order(self) -> 'List[_2025.SpecifiedParallelPartGroupDrawingOrder]':
        '''List[SpecifiedParallelPartGroupDrawingOrder]: 'ParallelPartGroupsDrawingOrder' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ParallelPartGroupsDrawingOrder, constructor.new(_2025.SpecifiedParallelPartGroupDrawingOrder))
        return value

    @property
    def parallel_part_groups(self) -> 'List[_2030.ParallelPartGroup]':
        '''List[ParallelPartGroup]: 'ParallelPartGroups' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ParallelPartGroups, constructor.new(_2030.ParallelPartGroup))
        return value
