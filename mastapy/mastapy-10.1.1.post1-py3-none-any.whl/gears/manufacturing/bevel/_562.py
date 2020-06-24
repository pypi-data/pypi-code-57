'''_562.py

ConicalGearMicroGeometryConfigBase
'''


from mastapy.gears.manufacturing.bevel import _580
from mastapy._internal import constructor
from mastapy.gears.analysis import _952
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MICRO_GEOMETRY_CONFIG_BASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalGearMicroGeometryConfigBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearMicroGeometryConfigBase',)


class ConicalGearMicroGeometryConfigBase(_952.GearImplementationDetail):
    '''ConicalGearMicroGeometryConfigBase

    This is a mastapy class.
    '''

    TYPE = _CONICAL_GEAR_MICRO_GEOMETRY_CONFIG_BASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalGearMicroGeometryConfigBase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def flank_measurement_border(self) -> '_580.FlankMeasurementBorder':
        '''FlankMeasurementBorder: 'FlankMeasurementBorder' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_580.FlankMeasurementBorder)(self.wrapped.FlankMeasurementBorder) if self.wrapped.FlankMeasurementBorder else None
