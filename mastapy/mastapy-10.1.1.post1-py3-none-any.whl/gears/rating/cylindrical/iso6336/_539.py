'''_539.py

ISO6336MeanStressInfluenceFactor
'''


from mastapy._internal import constructor, conversion
from mastapy.gears import _295
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_ISO6336_MEAN_STRESS_INFLUENCE_FACTOR = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ISO6336MeanStressInfluenceFactor')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO6336MeanStressInfluenceFactor',)


class ISO6336MeanStressInfluenceFactor(_1.APIBase):
    '''ISO6336MeanStressInfluenceFactor

    This is a mastapy class.
    '''

    TYPE = _ISO6336_MEAN_STRESS_INFLUENCE_FACTOR
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISO6336MeanStressInfluenceFactor.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def load_per_unit_face_width_of_the_lower_loaded_flank(self) -> 'float':
        '''float: 'LoadPerUnitFaceWidthOfTheLowerLoadedFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadPerUnitFaceWidthOfTheLowerLoadedFlank

    @property
    def load_per_unit_face_width_of_the_higher_loaded_flank(self) -> 'float':
        '''float: 'LoadPerUnitFaceWidthOfTheHigherLoadedFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadPerUnitFaceWidthOfTheHigherLoadedFlank

    @property
    def higher_loaded_flank(self) -> '_295.CylindricalFlanks':
        '''CylindricalFlanks: 'HigherLoadedFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.HigherLoadedFlank)
        return constructor.new(_295.CylindricalFlanks)(value) if value else None

    @property
    def stress_ratio(self) -> 'float':
        '''float: 'StressRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StressRatio

    @property
    def mean_stress_ratio(self) -> 'float':
        '''float: 'MeanStressRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanStressRatio

    @property
    def stress_influence_factor(self) -> 'float':
        '''float: 'StressInfluenceFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StressInfluenceFactor
