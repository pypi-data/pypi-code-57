'''_1621.py

LoadedCylindricalRollerBearingRow
'''


from mastapy.scripting import _6504
from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1620, _1636
from mastapy._internal.python_net import python_net_import

_LOADED_CYLINDRICAL_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedCylindricalRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedCylindricalRollerBearingRow',)


class LoadedCylindricalRollerBearingRow(_1636.LoadedNonBarrelRollerBearingRow):
    '''LoadedCylindricalRollerBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_CYLINDRICAL_ROLLER_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedCylindricalRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def rib_normal_contact_stress_inner_left(self) -> '_6504.SMTBitmap':
        '''SMTBitmap: 'RibNormalContactStressInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6504.SMTBitmap)(self.wrapped.RibNormalContactStressInnerLeft) if self.wrapped.RibNormalContactStressInnerLeft else None

    @property
    def rib_normal_contact_stress_inner_right(self) -> '_6504.SMTBitmap':
        '''SMTBitmap: 'RibNormalContactStressInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6504.SMTBitmap)(self.wrapped.RibNormalContactStressInnerRight) if self.wrapped.RibNormalContactStressInnerRight else None

    @property
    def rib_normal_contact_stress_outer_left(self) -> '_6504.SMTBitmap':
        '''SMTBitmap: 'RibNormalContactStressOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6504.SMTBitmap)(self.wrapped.RibNormalContactStressOuterLeft) if self.wrapped.RibNormalContactStressOuterLeft else None

    @property
    def rib_normal_contact_stress_outer_right(self) -> '_6504.SMTBitmap':
        '''SMTBitmap: 'RibNormalContactStressOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6504.SMTBitmap)(self.wrapped.RibNormalContactStressOuterRight) if self.wrapped.RibNormalContactStressOuterRight else None

    @property
    def loaded_bearing(self) -> '_1620.LoadedCylindricalRollerBearingResults':
        '''LoadedCylindricalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1620.LoadedCylindricalRollerBearingResults)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None
