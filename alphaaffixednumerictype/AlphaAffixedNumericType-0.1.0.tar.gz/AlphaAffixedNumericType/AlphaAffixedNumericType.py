import sys
import os
sys.path.append(os.path.dirname(__file__))

from .exceptions import NumericArithmeticException
import re


class AlphaAffixedNumericType():
    '''
    NOTE: 'aant' for short
    Support arithmetic with different data types
    '''
    ALPHA_AFFIXED_NUMERIC_TYPE_REGEX = r"^([a-zA-Z]*)(\d+)([a-zA-Z]*)$"
    INDEX_OF_PREFIX_GROUP = 0
    INDEX_OF_NUMBER_GROUP = 1
    INDEX_OF_POSTFIX_GROUP = 2

    def __init__(self, aant):
        # TODO: add variable to keep number of digits?
        self.mo = re.match(AlphaAffixedNumericType.ALPHA_AFFIXED_NUMERIC_TYPE_REGEX, aant)
        assert aant.isalnum(), f'String "{aant}" is not alphanumeric'
        assert self.mo, f'String "{aant}" is not affixed'
        self.aant = aant

    def get_value(self):
        return self.aant

    def get_prefix_part_of_aant(self):
        return self.mo.groups()[AlphaAffixedNumericType.INDEX_OF_PREFIX_GROUP]

    def get_numeric_part_of_aant(self):
        '''
        :returns numeric part of type, in string format
        '''
        return self.mo.groups()[AlphaAffixedNumericType.INDEX_OF_NUMBER_GROUP]

    def get_postfix_part_of_aant(self):
        return self.mo.groups()[AlphaAffixedNumericType.INDEX_OF_POSTFIX_GROUP]

    @staticmethod
    def add_int_list(int_list_1, int_list_2):
        l1 = len(int_list_1)
        l2 = len(int_list_2)
        if l2 > l1:
            int_list_1 = [0] * (l2 - l1) + int_list_1
        elif l1 > l2:
            int_list_2 = [0] * (l1 - l2) + int_list_2

        carry, n1, n2 = 0, 0, 0

        for i in range(len(int_list_1) - 1, -1 , -1):
            n1 = int_list_1[i]
            n2 = int_list_2[i]
            s = n1 + n2 + carry
            carry = s // 10
            int_list_1[i] = s % 10
        
        if carry > 0:
            int_list_1 = [carry] + int_list_1
        
        return int_list_1
    
    def has_same_affix(self, other):
        assert isinstance(other, AlphaAffixedNumericType), f'Type error: not type AlphaAffixedNumericType'
        return \
            self.get_prefix_part_of_aant() == other.get_prefix_part_of_aant() \
            and \
            self.get_postfix_part_of_aant() == other.get_postfix_part_of_aant()

    def __add__(self, other):
        '''
        Increament numeric part of the type. 
        e.g. AlphanumericType("A130") + 1 = AlphanumericType("A131")
        :param other: whole number
        '''
        assert str(other).isdigit(), f'Operand "{other}" is not a valid number'
        other = [int(d) for d in str(other)]

        numeric_part_of_aant = self.get_numeric_part_of_aant()
        numeric_part_of_aant = [int(d) for d in str(numeric_part_of_aant)]

        new_numeric_part_of_aant = ''.join(
            [
                str(i) for i in AlphaAffixedNumericType.add_int_list(
                                other,
                                numeric_part_of_aant
                            )
            ]
        )

        return AlphaAffixedNumericType(
            self.get_prefix_part_of_aant() + \
            new_numeric_part_of_aant + \
            self.get_postfix_part_of_aant()
        )

    def __sub__(self, other):
        '''
        :returns int if other is same type, AlphaAffixedNumericType if other is
        of str or int type
        '''
        type_of_other = type(other)
        assert (type_of_other == AlphaAffixedNumericType and self.has_same_affix(other)) \
            or (type_of_other == str and str(other).isdigit()) \
            or type_of_other == int \
            , f'Invalid operand {other}'
        
        diff = -1  # TODO: 0 or -1?

        if type_of_other == AlphaAffixedNumericType:
            return int(self.get_numeric_part_of_aant()) - int(other.get_numeric_part_of_aant())
        elif type_of_other == str or type_of_other == int:
            diff = int(self.get_numeric_part_of_aant()) - int(other)
            if diff < 0:
                raise NumericArithmeticException(f'Numeric part of "{self.get_value()}" is less than {other}')

            return AlphaAffixedNumericType(
                self.get_prefix_part_of_aant() + \
                str(diff) + \
                self.get_postfix_part_of_aant()
            )
        else:
            raise Exception(f'Invalid operand {other}')

    def __repr__(self):
        return f'{self.__class__} - <value {self.aant}>'
    
    def __str__(self):
        return self.aant
