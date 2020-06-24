'''_1672.py

LoadedFluidFilmBearingPad
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_LOADED_FLUID_FILM_BEARING_PAD = python_net_import('SMT.MastaAPI.Bearings.BearingResults.FluidFilm', 'LoadedFluidFilmBearingPad')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedFluidFilmBearingPad',)


class LoadedFluidFilmBearingPad(_1.APIBase):
    '''LoadedFluidFilmBearingPad

    This is a mastapy class.
    '''

    TYPE = _LOADED_FLUID_FILM_BEARING_PAD
    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedFluidFilmBearingPad.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def pad_id(self) -> 'str':
        '''str: 'PadID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PadID

    @property
    def misalignment(self) -> 'float':
        '''float: 'Misalignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Misalignment
