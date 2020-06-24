'''_1062.py

DIN3967SystemOfGearFits
'''


from mastapy.gears.gear_designs.cylindrical import _987, _988
from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DIN3967_SYSTEM_OF_GEAR_FITS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances', 'DIN3967SystemOfGearFits')


__docformat__ = 'restructuredtext en'
__all__ = ('DIN3967SystemOfGearFits',)


class DIN3967SystemOfGearFits(_1.APIBase):
    '''DIN3967SystemOfGearFits

    This is a mastapy class.
    '''

    TYPE = _DIN3967_SYSTEM_OF_GEAR_FITS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DIN3967SystemOfGearFits.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def tooth_thickness_reduction_allowance(self) -> '_987.DIN3967AllowanceSeries':
        '''DIN3967AllowanceSeries: 'ToothThicknessReductionAllowance' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ToothThicknessReductionAllowance)
        return constructor.new(_987.DIN3967AllowanceSeries)(value) if value else None

    @tooth_thickness_reduction_allowance.setter
    def tooth_thickness_reduction_allowance(self, value: '_987.DIN3967AllowanceSeries'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ToothThicknessReductionAllowance = value

    @property
    def tooth_thickness_tolerance(self) -> '_988.DIN3967ToleranceSeries':
        '''DIN3967ToleranceSeries: 'ToothThicknessTolerance' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ToothThicknessTolerance)
        return constructor.new(_988.DIN3967ToleranceSeries)(value) if value else None

    @tooth_thickness_tolerance.setter
    def tooth_thickness_tolerance(self, value: '_988.DIN3967ToleranceSeries'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ToothThicknessTolerance = value
