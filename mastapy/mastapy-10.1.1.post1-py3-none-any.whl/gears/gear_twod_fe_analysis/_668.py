'''_668.py

CylindricalGearSetTIFFAnalysis
'''


from mastapy.gears.analysis import _957
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_TIFF_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.GearTwoDFEAnalysis', 'CylindricalGearSetTIFFAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetTIFFAnalysis',)


class CylindricalGearSetTIFFAnalysis(_957.GearSetDesignAnalysis):
    '''CylindricalGearSetTIFFAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_TIFF_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetTIFFAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
