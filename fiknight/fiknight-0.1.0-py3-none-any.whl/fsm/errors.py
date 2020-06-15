#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright (C) 2020  Trijeet Sethi
#This project is written under the GPL license. For the full GPL license, please see the base directory COPYING file or visit <https://www.gnu.org/licenses/>.

class FSError(Exception):
    """Base class for exceptions raised by FiKnight."""
    pass

class ConstructorError(FSError):
    """
    Exception raised for invalid inputs into constructor methods.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    # def __init__(self, expression, message) -> None:
    #     self.expression = expression
    #     self.message = message
    pass