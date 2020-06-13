"""An example of abstract class

An example of abstract class. If you need to use a framework, abstract class is a good method.
There is a random boolean by baz function and an abstract method named foo function.
It is not possible to instantiate a class with an abstract method.
And it is not possible to have an abstract method protected: it will be changed in a pubilc method.

# license MIT
# author Alessandra Bilardi <alessandra.bilardi@gmail.com>
# see https://github.com/bilardi/python-prototype for details
# cite https://www.python.org/dev/peps/pep-3119/

Much of the thinking that went into the proposal is not about the specific mechanism of ABCs,
as contrasted with Interfaces or Generic Functions (GFs), but about clarifying philosophical issues
like "what makes a set", "what makes a mapping" and "what makes a sequence".
ABCs are intended to solve problems that don't have a good solution at all in Python 2,
such as distinguishing between mappings and sequences.
"""

from abc import ABCMeta, abstractmethod
import random

class MyClassAbstract(metaclass=ABCMeta):
    """
    An example of abstract class. If you need to use a framework, abstract class is a good method.
    There is a random boolean by baz function and an abstract method named foo function.
    It is not possible to instantiate a class with an abstract method.
    And it is not possible to have an abstract method protected: it will be changed in a pubilc method.
    """
    def baz(self):
        """
        Baz gets a random boolean
            Returns:
                A random boolean value
        """
        return bool(random.getrandbits(1))

    @abstractmethod
    def foo(self, foo) -> bool:
        """
        Foo
            Args:
                foo(bool): a boolean value
            Returns:
                A boolean value
            Raises:
                NotImplementedError
        """
        raise NotImplementedError
