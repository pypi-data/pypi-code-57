'''_634.py

MicroGeometryInputsLead
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical import _633, _632
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_INPUTS_LEAD = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'MicroGeometryInputsLead')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryInputsLead',)


class MicroGeometryInputsLead(_633.MicroGeometryInputs['_632.LeadModificationSegment']):
    '''MicroGeometryInputsLead

    This is a mastapy class.
    '''

    TYPE = _MICRO_GEOMETRY_INPUTS_LEAD
    __hash__ = None

    def __init__(self, instance_to_wrap: 'MicroGeometryInputsLead.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def number_of_lead_segments(self) -> 'int':
        '''int: 'NumberOfLeadSegments' is the original name of this property.'''

        return self.wrapped.NumberOfLeadSegments

    @number_of_lead_segments.setter
    def number_of_lead_segments(self, value: 'int'):
        self.wrapped.NumberOfLeadSegments = int(value) if value else 0
