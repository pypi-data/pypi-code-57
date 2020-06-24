'''_2389.py

FlexibleGearChart
'''


from mastapy._internal import constructor
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.analyses_and_results.system_deflections import _2376
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_GEAR_CHART = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting', 'FlexibleGearChart')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexibleGearChart',)


class FlexibleGearChart(_1.APIBase):
    '''FlexibleGearChart

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_GEAR_CHART
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexibleGearChart.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def remove_rigid_body_motion(self) -> 'bool':
        '''bool: 'RemoveRigidBodyMotion' is the original name of this property.'''

        return self.wrapped.RemoveRigidBodyMotion

    @remove_rigid_body_motion.setter
    def remove_rigid_body_motion(self, value: 'bool'):
        self.wrapped.RemoveRigidBodyMotion = bool(value) if value else False

    @property
    def planets(self) -> 'list_with_selected_item.ListWithSelectedItem_CylindricalGearSystemDeflection':
        '''list_with_selected_item.ListWithSelectedItem_CylindricalGearSystemDeflection: 'Planets' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_CylindricalGearSystemDeflection)(self.wrapped.Planets) if self.wrapped.Planets else None

    @planets.setter
    def planets(self, value: 'list_with_selected_item.ListWithSelectedItem_CylindricalGearSystemDeflection.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_CylindricalGearSystemDeflection.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_CylindricalGearSystemDeflection.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.Planets = value
