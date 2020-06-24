"""
This submodule containts functionality to store and manipulate quantities that
can be either purely numerical, numerical with units, or purely descriptive.
The Quantity object is used to store what type of quantity and to handle
quantity addition. The `largest_quantity` function is used instead of
`max(quantity1, quantity2)` as lagrest quantity sets a new output that is
equal to neither of the inputs when the answer is ambiguous.
"""

import re
from copy import copy
import math
from fractions import Fraction
import logging
from gitbuilding.buildup.unit import UnitLibrary

_LOGGER = logging.getLogger('BuildUp')
UNIT_LIB = UnitLibrary()

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
            return numerical_quantity(max(q1.value, q2.value))
        if q1.type == Quantity.NUMERICAL_UNIT:
            if q1.unit == q2.unit:
                return numerical_unit_quantity(max(q1.value, q2.value),
                                               q1.unit)
            if UNIT_LIB.convertable(q1.unit, q2.unit):
                q1c, q2c = unify_units(q1, q2)
                if q1c.value > q2c.value:
                    return copy(q1)
                return copy(q2)
    _LOGGER.warning('No rules known for comparing %s to %s, setting total to "Some"',
                    q1,
                    q2)
    return descriptive_quantity("Some")

def unify_units(q1, q2):
    """
    This function takes two Quantity objects and converts them to the same
    unit. The unit will be in first UnitGroup the that is parent of both input
    UnitGroups
    """
    if q1.type != Quantity.NUMERICAL_UNIT or q2.type != Quantity.NUMERICAL_UNIT:
        raise ValueError('Can only unify units for Quantities that are NUMERICAL_UNIT type')
    scale1, scale2, new_unit = UNIT_LIB.unify_units(q1.unit, q2.unit)
    q1_converted = numerical_unit_quantity(q1.value*scale1, new_unit.name)
    q2_converted = numerical_unit_quantity(q2.value*scale2, new_unit.name)
    return q1_converted, q2_converted

def _close_enough(value1, value2, tol=5):
    """
    Just like equals except only checks that the values are within a part in
    10^tol of eachother. 10^5 is standard.
    """
    if (not isinstance(value1, (int, float, Fraction)) or
            not isinstance(value2, (int, float, Fraction))):
        return TypeError('_close_enough only supports int, float, or Fraction '
                         'values')
    if value1 == value2:
        return True
    max_value = max(value1, value2)
    diff = abs(value1-value2)
    log_diff = math.log10(diff) - math.log10(max_value)
    return log_diff < -tol

def descriptive_quantity(description):
    """
    returns a Quantity with Quantity.type=Quantity.DESCRIPTIVE
    with the description as input
    """
    return Quantity({'type': Quantity.DESCRIPTIVE,
                     'description': description,
                     'value': None,
                     'unit': None})

def numerical_quantity(value):
    """
    returns a Quantity with Quantity.type=Quantity.NUMERICAL
    with the value as input
    """
    return Quantity({'type': Quantity.NUMERICAL,
                     'description': None,
                     'value': value,
                     'unit': None})

def numerical_unit_quantity(value, unit):
    """
    returns a Quantity with Quantity.type=Quantity.NUMERICAL_UNIT
    with the value as input
    """
    return Quantity({'type': Quantity.NUMERICAL_UNIT,
                     'description': None,
                     'value': value,
                     'unit': unit})


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

    DENOM_PRINT_LIST = [2, 3, 4, 5, 6, 8, 12, 16, 32, 64, 128]

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
        value = self.value
        if isinstance(value, Fraction):
            num = value.numerator
            denom = value.denominator
            if denom not in self.DENOM_PRINT_LIST:
                if num == denom:
                    value = int(value)
                else:
                    value = float(value)
            else:
                if value > 1:
                    int_val = num//denom
                    return str(int_val)+' '+str(value-int_val)
        if isinstance(value, float):
            round_to_n = lambda x, n: round(x, -int(math.floor(math.log10(x))) + (n - 1))
            value = round_to_n(value, 4)
        return str(value)

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
        if isinstance(other, Quantity):
            return self._eq_quantity(other)
        if isinstance(other, (int, float, Fraction)):
            if self.type == self.NUMERICAL:
                return _close_enough(self.value, other)
            return False
        if isinstance(other, (str)):
            return self == Quantity(other)
        return NotImplemented

    def _eq_quantity(self, other):
        """
        Implents __eq__ if other is also Quantity
        """
        if self.type != other.type:
            return False
        if self.type == self.INVALID:
            return False
        if self.type == self.DESCRIPTIVE:
            return self.description == other.description
        if self.type == self.NUMERICAL:
            return _close_enough(self.value, other.value)
        return self._eq_unit(other)

    def _eq_unit(self, other):
        """
        Implents __eq__ for type==NUMERICAL_UNIT
        """
        if self.unit == other.unit:
            return _close_enough(self.value, other.value)
        if not UNIT_LIB.convertable(self.unit, other.unit):
            return False
        self_conv, other_conv = unify_units(self, other)
        return _close_enough(self_conv.value, other_conv.value)

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if isinstance(other, Quantity):
            return self._add_quantity(other)
        if isinstance(other, str):
            return self + Quantity(other)
        if isinstance(other, (int, float, Fraction)):
            if self.type == self.NUMERICAL:
                return numerical_quantity(self.value+other)
        raise RuntimeError(f'Cannot add value of type {type(other)} to a {self.type} '
                           'Quantity')

    def _add_quantity(self, other):
        """
        Implents __add__ if other is also Quantity
        """
        if self.INVALID in [self.type, other.type]:
            raise RuntimeError('Cannot add invalid quantities.')
        if self.type == other.type:
            if self.type == self.NUMERICAL:
                return numerical_quantity(self.value+other.value)
            if self.type == self.NUMERICAL_UNIT:
                return self._add_unit(other)
        _LOGGER.warning('No rules known for adding %s to %s, setting total to "Some"',
                        self,
                        other)
        return descriptive_quantity("Some")

    def _add_unit(self, other):
        """
        Implents __add__ if other is also Quantity.type == NUMERICAL_UNIT
        """
        if self.unit == other.unit:
            return numerical_unit_quantity(self.value+other.value, self.unit)
        if UNIT_LIB.convertable(self.unit, other.unit):
            q1, q2 = unify_units(self, other)
            total = q1 + q2
            total.auto_scale()
            return total
        _LOGGER.warning('No rules known for adding quantities with units %s and %s, '
                        'setting total to "Some"',
                        self.unit,
                        other.unit)
        return descriptive_quantity("Some")

    def auto_scale(self):
        """
        Auto scale the quantity to a more appropriate unit in the same UnitGroup.
        This may change the formatting of the unit string.
        """
        if self.type == self.NUMERICAL_UNIT:
            try:
                self._value, unit_obj = UNIT_LIB.scale_quantity(self.value, self.unit)
                self._unit = unit_obj.name
            except RuntimeError:
                # Runtime error is unit scaling is not known.
                pass
