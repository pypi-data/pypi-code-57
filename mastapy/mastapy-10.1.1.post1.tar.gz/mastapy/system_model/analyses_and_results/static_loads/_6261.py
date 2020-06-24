'''_6261.py

DataFromJMAGPerMeanTorque
'''


from mastapy._internal import constructor
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_DATA_FROM_JMAG_PER_MEAN_TORQUE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'DataFromJMAGPerMeanTorque')


__docformat__ = 'restructuredtext en'
__all__ = ('DataFromJMAGPerMeanTorque',)


class DataFromJMAGPerMeanTorque(_1.APIBase):
    '''DataFromJMAGPerMeanTorque

    This is a mastapy class.
    '''

    TYPE = _DATA_FROM_JMAG_PER_MEAN_TORQUE
    __hash__ = None

    def __init__(self, instance_to_wrap: 'DataFromJMAGPerMeanTorque.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def mean_torque(self) -> 'float':
        '''float: 'MeanTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeanTorque
