'''_1399.py

MomentInputComponent
'''


from mastapy._internal import constructor
from mastapy.nodal_analysis.varying_input_components import _1396
from mastapy._internal.python_net import python_net_import

_MOMENT_INPUT_COMPONENT = python_net_import('SMT.MastaAPI.NodalAnalysis.VaryingInputComponents', 'MomentInputComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('MomentInputComponent',)


class MomentInputComponent(_1396.AbstractVaryingInputComponent):
    '''MomentInputComponent

    This is a mastapy class.
    '''

    TYPE = _MOMENT_INPUT_COMPONENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MomentInputComponent.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def moment(self) -> 'float':
        '''float: 'Moment' is the original name of this property.'''

        return self.wrapped.Moment

    @moment.setter
    def moment(self, value: 'float'):
        self.wrapped.Moment = float(value) if value else 0.0
