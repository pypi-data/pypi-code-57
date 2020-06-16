"""A set of semantic-less decorations that are used to pinpoint functions
that the VPL design plugin will modify to generate student requested files
or genarate test comparator files."""


def todoin(_func=None, *, comment=None):
    """States that a function body should be removed from the student requested
    file, while keeping its declaration and profile + documentation.
    WARNING : all comments that begins the body will be kept as/with the docstring."""

    def decorator_todoin(func):
      return func

    if _func is None:
      return decorator_todoin
    else:
      return decorator_todoin(_func)


def todo(_func=None, *, comment=None):
    """States that a function should be entirely removed from the student
    requested file. If keyword comment is provided, then a comment with the
    specified content will be added in place of the function."""

    def decorator_todo(func):
        return func

    if _func is None:
        return decorator_todo
    else:
        return decorator_todo(_func)


def relative_evaluation(_func=None, *, grade=None):
    """When this decoration is present on at least one object in the set of test files,
    then all grades are considered as relative.
    The optional grade argument represents the maximum grade to be obtained for the whole Lab.
    All grade decorations in all test files will be interpreted as relative grades.
    If several relative_evaluation decoration is present in the set of test files, then one of
    them (actual one is not predictable) will be taken into account."""

    def decorator_relative_evaluation(func):
        return func

    if _func is None:
        return decorator_relative_evaluation
    else:
        return decorator_relative_evaluation(_func)