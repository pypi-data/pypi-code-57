"""
This submodule containts functionality to store and manipulate quantities that
can be either purely numerical, numerical with units, or purely descriptive.
The Quantity object is used to store what type of quantity and to handle
quantity addition. The `largest_quantity` function is used instead of
`max(quantity1, quantity2)` as lagrest quantity sets a new output that is
equal to neither of the inputs when the answer is ambiguous.
"""

import re
from fractions import Fraction
import logging

_LOGGER = logging.getLogger('BuildUp')

def _to_number(value_string):
    """
    Input is a string which is either a number or a fraction.
    Output is a either an int, a float, a Fraction object.
    """
    if '.' in value_string:
        return float(value_string)
    if '/' in value_string:
        strings = value_string.split(' ')
        if len(strings) == 1:
            return Fraction(value_string)
        if len(strings) == 2:
            return int(strings[0])+Fraction(strings[1])
        raise ValueError(f'Cannot parse "{value_string}" to a number')
    return int(value_string)

def largest_quantity(q1, q2):
    """
    This function finds the maximum of two quantities of any class.
    This is done by trying it's level best compare them and if it fails it
    returns the string "Some". You cannot use `max` on Quantity objects as
    we need the ability to create a new value when it is ambiguous.
    """

    if not (isinstance(q1, Quantity) and isinstance(q2, Quantity)):
        raise TypeError('q1 and q2 must be Quantity objects.')
    if Quantity.INVALID in [q1.type, q2.type]:
        raise RuntimeError('Cannot compare invalid quantities.')

    if q1.type == q2.type:
        if q1.type == Quantity.NUMERICAL:
            return Quantity({'type': Quantity.NUMERICAL,
                             'description': None,
                             'value': max(q1.value, q2.value),
                             'unit': None})
        if q1.type == Quantity.NUMERICAL_UNIT:
            if q1.unit == q2.unit:
                return Quantity({'type': Quantity.NUMERICAL_UNIT,
                                 'description': None,
                                 'value': max(q1.value, q2.value),
                                 'unit': q1.unit})
    _LOGGER.warning('No rules known for comparing %s to %s, setting total to "Some"',
                    q1,
                    q2)
    return Quantity({'type': Quantity.DESCRIPTIVE,
                     'description': "Some",
                     'value': None,
                     'unit': None})


class Quantity:
    """
    A quantity objects represents the quantity for a part. The quantity object is
    responsible for interpreting the incoming quantity string. It can hold numerical
    quantities with and without units, as well as descriptive quantities.
    Input to constructor is the quantity string from the BuildUp file.
    """

    INVALID = -1
    NUMERICAL = 0
    NUMERICAL_UNIT = 1
    DESCRIPTIVE = 2
    def __init__(self, qty):
        self._description = None
        self._unit = None
        self._value = None
        self._type = self.INVALID
        if isinstance(qty, str):
            if qty == '':
                return
            self._interpret_string(qty)
        elif isinstance(qty, dict):
            try:
                self._description = qty['description']
                self._unit = qty['unit']
                self._value = qty['value']
                self._type = qty['type']
            except KeyError:
                raise ValueError('Invalid dictionary passed to Quantity constructor')

    @property
    def valid(self):
        """
        Read only property describing if the quantity is valid. Note that ambiguous
        quantities (Descriptive quantity "Some") from addition and comparisons are
        still valid.
        """
        return self.type != self.INVALID

    @property
    def description(self):
        """
        Read only property that returns the description string of the quantity. This is
        None if Quantity.type is not Quantity.DESCRIPTIVE
        """
        return self._description

    @property
    def value(self):
        """
        Read only property that returns the numerical value of the quantity, this is None
        if Quantity.type is not Quantity.NUMERICAL or Quantity.NUMERICAL_UNIT. The type
        of the value will be one of int, float, Fraction.
        """
        return self._value

    @property
    def unit(self):
        """
        Read only property that returns the unit string of the quantity. This is None if
        Quantity.type is not Quantity.NUMERICAL_UNIT.
        """
        return self._unit

    @property
    def type(self):
        """
        Read only property that returns the type of quantity that the object holds. This
        should be one of Quantity.DESCRIPTIVE, Quantity.NUMERICAL, Quantity.NUMERICAL_UNIT
        but it can also be Quantity.INVALID if the input to the constructor was not valid.
        """
        return self._type

    def __str__(self):
        if self.type == self.INVALID:
            return "INVALID QUANTITY"
        if self.type == self.DESCRIPTIVE:
            return self.description
        if self.type == self.NUMERICAL:
            return self._formatted_value
        return self._formatted_value+' '+self.unit+' of'

    def __repr__(self):
        return str(self)

    @property
    def _formatted_value(self):
        if isinstance(self.value, Fraction) and self.value > 1:
            num = self.value.numerator
            denom = self.value.denominator
            int_val = num//denom
            return str(int_val)+' '+str(self.value-int_val)
        return str(self.value)

    def _interpret_string(self, qty_string):
        match = re.match(r'^([0-9]+|[0-9]*\.[0-9]+|(?:[0-9]+ )?[0-9]+\/[0-9]+)?'
                         r' *([^\/\.0-9\s].*)?$',
                         qty_string)
        if match is None:
            self._type = self.DESCRIPTIVE
            self._description = qty_string
            _LOGGER.warning('Quantity "%s" appears to be a malformed value and unit.'
                            ' It will be treated a literal string.',
                            qty_string)
            return
        if match.group(1) in ['', None]:
            self._type = self.DESCRIPTIVE
            self._description = match.group(2)
        elif match.group(2) in ['', None]:
            self._type = self.NUMERICAL
            self._value = _to_number(match.group(1))
        else:
            self._type = self.NUMERICAL_UNIT
            self._value = _to_number(match.group(1))
            self._unit = match.group(2)

    def __eq__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        if self.type != other.type:
            return False
        if self.description != other.description:
            return False
        if self.value != other.value:
            return False
        if self.unit != other.unit:
            return False
        return True

    def __add__(self, other):
        if not isinstance(other, Quantity):
            return NotImplemented
        if self.INVALID in [self.type, other.type]:
            raise RuntimeError('Cannot add invalid quantities.')
        if self.type == other.type:
            if self.type == self.NUMERICAL:
                return Quantity({'type': self.NUMERICAL,
                                 'description': None,
                                 'value': self.value+other.value,
                                 'unit': None})
            if self.type == self.NUMERICAL_UNIT:
                if self.unit == other.unit:
                    return Quantity({'type': self.NUMERICAL_UNIT,
                                     'description': None,
                                     'value': self.value+other.value,
                                     'unit': self.unit})
        _LOGGER.warning('No rules known for adding %s to %s, setting total to "Some"',
                        self,
                        other)
        return Quantity({'type': self.DESCRIPTIVE,
                         'description': "Some",
                         'value': None,
                         'unit': None})
