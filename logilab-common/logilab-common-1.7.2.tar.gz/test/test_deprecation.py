# copyright 2003-2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-common.
#
# logilab-common is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# logilab-common is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-common.  If not, see <http://www.gnu.org/licenses/>.
"""unit tests for logilab.common.deprecation"""

import warnings

from logilab.common.testlib import TestCase, unittest_main
from logilab.common.modutils import LazyObject
from logilab.common import deprecation


class RawInputTC(TestCase):

    # XXX with 2.6 we could test warnings
    # http://docs.python.org/library/warnings.html#testing-warnings
    # instead we just make sure it does not crash

    def mock_warn(self, *args, **kwargs):
        self.messages.append(args[0])

    def setUp(self):
        self.messages = []
        deprecation.warn = self.mock_warn

    def tearDown(self):
        deprecation.warn = warnings.warn

    def mk_func(self):
        def any_func():
            pass

        return any_func

    def test_class_deprecated(self):
        class AnyClass(object, metaclass=deprecation.class_deprecated):
            pass

        AnyClass()
        self.assertEqual(self.messages, ["[test_deprecation] AnyClass is deprecated"])

    def test_class_renamed(self):
        class AnyClass(object):
            pass

        OldClass = deprecation.class_renamed("OldClass", AnyClass)

        OldClass()
        self.assertEqual(
            self.messages, ["[test_deprecation] OldClass is deprecated, use AnyClass instead"]
        )

    def test_class_renamed_conflict_metaclass(self):
        class SomeMetaClass(type):
            pass

        class AnyClass(metaclass=SomeMetaClass):
            pass

        # make sure the "metaclass conflict: the metaclass of a derived class # must be a
        # (non-strict) subclass of the metaclasses of all its bases" exception won't be raised
        deprecation.class_renamed("OldClass", AnyClass)

    def test_class_moved(self):
        class AnyClass(object):
            pass

        OldClass = deprecation.class_moved(new_class=AnyClass, old_name="OldName")
        OldClass()
        self.assertEqual(
            self.messages,
            ["[test_deprecation] class OldName is now available as test_deprecation.AnyClass"],
        )

        self.messages = []

        AnyClass = deprecation.class_moved(new_class=AnyClass)

        AnyClass()
        self.assertEqual(
            self.messages,
            ["[test_deprecation] class AnyClass is now available as test_deprecation.AnyClass"],
        )

    def test_deprecated_func(self):
        any_func = deprecation.callable_deprecated()(self.mk_func())
        any_func()
        any_func = deprecation.callable_deprecated("message")(self.mk_func())
        any_func()
        self.assertEqual(
            self.messages,
            [
                '[test_deprecation] The function "any_func" is deprecated',
                "[test_deprecation] message",
            ],
        )

    def test_deprecated_decorator(self):
        @deprecation.callable_deprecated()
        def any_func():
            pass

        any_func()

        @deprecation.callable_deprecated("message")
        def any_func():
            pass

        any_func()
        self.assertEqual(
            self.messages,
            [
                '[test_deprecation] The function "any_func" is deprecated',
                "[test_deprecation] message",
            ],
        )

    def test_deprecated_decorator_bad_lazyobject(self):
        # this should not raised an ImportationError
        deprecation.deprecated("foobar")(LazyObject("cubes.localperms", "xperm"))

        # with or without giving it a message (because it shouldn't access
        # attributes of the wrapped object before the object is called)
        deprecation.deprecated()(LazyObject("cubes.localperms", "xperm"))

        # all of this is done because of the magical way LazyObject is working
        # and that sometime CW used to use it to do fake import on deprecated
        # modules to raise a warning if they were used but not importing them
        # by default.
        # See: https://forge.extranet.logilab.fr/cubicweb/cubicweb/blob/3.24.0/cubicweb/schemas/__init__.py#L51 # noqa

    def test_attribute_renamed(self):
        @deprecation.attribute_renamed(old_name="old", new_name="new")
        class SomeClass:
            def __init__(self):
                self.new = 42

        some_class = SomeClass()
        self.assertEqual(some_class.old, some_class.new)
        self.assertEqual(
            self.messages,
            [
                "[test_deprecation] SomeClass.old has been renamed and is deprecated, "
                "use SomeClass.new instead"
            ],
        )

        some_class.old = 43
        self.assertEqual(some_class.old, 43)
        self.assertEqual(some_class.old, some_class.new)

        self.assertTrue(hasattr(some_class, "new"))
        self.assertTrue(hasattr(some_class, "old"))
        del some_class.old
        self.assertFalse(hasattr(some_class, "new"))
        self.assertFalse(hasattr(some_class, "old"))

    def test_argument_renamed(self):
        @deprecation.argument_renamed(old_name="old", new_name="new")
        def some_function(new):
            return new

        self.assertEqual(some_function(new=42), 42)
        self.assertEqual(some_function(old=42), 42)
        self.assertEqual(
            self.messages,
            [
                "[test_deprecation] argument old of callable some_function has been renamed and is "
                "deprecated, use keyword argument new instead"
            ],
        )

        with self.assertRaises(ValueError):
            some_function(new=42, old=42)

    def test_argument_removed(self):
        @deprecation.argument_removed("old")
        def some_function(new):
            return new

        self.assertEqual(some_function(new=42), 42)
        self.assertEqual(some_function(new=10, old=20), 10)
        self.assertEqual(
            self.messages,
            [
                "[test_deprecation] argument old of callable some_function has been removed and is "
                "deprecated"
            ],
        )

    def test_callable_renamed(self):
        def any_func():
            pass

        old_func = deprecation.callable_renamed("old_func", any_func)
        old_func()

        self.assertEqual(
            self.messages,
            [
                "[test_deprecation] old_func has been renamed and is deprecated, "
                "uses any_func instead"
            ],
        )

    def test_moved(self):
        module = "data.deprecation"
        any_func = deprecation.callable_moved(module, "moving_target")
        any_func()
        self.assertEqual(
            self.messages,
            ["[test_deprecation] object moving_target has been moved to module data.deprecation"],
        )


if __name__ == "__main__":
    unittest_main()
