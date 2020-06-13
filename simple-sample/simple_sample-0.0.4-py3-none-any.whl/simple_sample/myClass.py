"""An example of class

An example of class that it extends an abstract class and it implements an interface.
There is a boolean pun by foo function of abstract class, bar function of interface class,
and foobar function of this class.

# license MIT
# author Alessandra Bilardi <alessandra.bilardi@gmail.com>
# see https://github.com/bilardi/python-prototype for details

Note that the _quux method is not present in the documentation like the other methods because it is a method protected.

    >>> from simple_sample.myClass import MyClass
    >>> help(MyClass)

# cite https://stackoverflow.com/questions/11483366/protected-method-in-python/11483397#11483397

Python does not support access protection as C++/Java/C# does. Everything is public.
The motto is, "We're all adults here." Document your classes, and insist that your collaborators read and follow the documentation.
The culture in Python is that names starting with underscores mean,
"don't use these unless you really know you should." You might choose to begin your "protected" methods with underscores.
But keep in mind, this is just a convention, it doesn't change how the method can be accessed.
"""

from simple_sample.myClassInterface import MyClassInterface
from simple_sample.myClassAbstract import MyClassAbstract

class MyClass(MyClassInterface, MyClassAbstract):
    """
    An example of class that it extends an abstract class and it implements an interface.
    There is a boolean pun by foo function of abstract class, bar function of interface class,
    and foobar function of this class.
        Args:
            bar(bool): a boolean value
    """
    # bar(bool): a class boolean variable with default True
    _bar = True

    def __init__(self, bar = True):
        """
        Initialization of variables
            Args:
                bar(bool): a boolean value
        """
        self._bar = bar

    def foo(self, foo):
        """
        Foo gets reverse value of foo
            Args:
                foo(bool): a boolean value
            Returns:
                The reverse value of foo
        """
        return not foo

    def bar(self):
        """
        Bar
            Returns:
                The boolean value of _bar
        """
        return self._bar

    def foobar(self):
        """
        Foobar gets reverse value of _bar
            Returns:
                The reverse value of _bar
        """
        return self.foo(self._bar)

    def _quux(self):
        """
        Quux recalls some methods
            Returns:
                The boolean value
        """
        try:
            if MyClassInterface.bar(self) is None:
                MyClassInterface.qux(self)
        except NotImplementedError:
            return self.baz()
        return True

    def fooquux(self):
        """
        Fooquux gets reverse value of protected method _quux
            Returns:
                The boolean value
        """
        return self.foo(self._quux())
