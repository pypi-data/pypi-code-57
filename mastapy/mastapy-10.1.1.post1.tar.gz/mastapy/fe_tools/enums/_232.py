'''_232.py

ElementPropertyClass
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTY_CLASS = python_net_import('SMT.MastaAPI.FETools.Enums', 'ElementPropertyClass')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertyClass',)


class ElementPropertyClass(Enum):
    '''ElementPropertyClass

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ELEMENT_PROPERTY_CLASS
    __hash__ = None

    UNDEFINED = 0
    SOLID = 1
    SHELL = 2
    MEMBRANE = 3
    BEAM = 4
    TRUSS = 5
    INFINITE = 6
    GAP = 7
    JOINT = 8
    SPRING_DASHPOT = 9
    RIGID = 10
    CONSTRAINT = 11
    PLOT = 12
    MASS = 13
    INTERFACE = 14
    SUPERELEMENT = 15
