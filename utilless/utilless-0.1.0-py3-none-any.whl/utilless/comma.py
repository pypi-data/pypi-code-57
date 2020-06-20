# comma.py
"""
Module: COMMA
manipulates different kinds of elements using commas

A very common use case is to get a list and put all its items
in a string separated by comma. [name, job, age] => 'name,job,age'
"""

def commator(iterable, binder=',', lastbinder=','):
    """
    Mother of other functions like justcomma and commaspace.
    Takes a iterable and returns a string
    with all the items separated by binder parameter
    """
    # raises error if iterable is empty
    if not iterable:
        raise ValueError('The iterable is empty')

    # turns all items of iterable into strings
    words = list(map(str, iterable))

    # join words with binder until before the last one,
    # which is on its turn bound with the lastbinder. See commaand
    return binder.join(words[:len(words) - 1]) + lastbinder + words[-1]

def justcomma(iterable):
    """
    Function that takes a iterable and returns a string
    with all the items separated by a comma
    Example:
    justcomma(['apples', 'bananas', 'tofu', 'cats']) =>
       'apples,bananas,tofu,cats'
    """
    return commator(iterable)

def commaspace(iterable):
    """
    Function that takes a iterable and returns a string
    with all the items separated by a comma and a space.
    Example:
    commaspace(['apples', 'bananas', 'tofu', 'cats']) =>
       'apples, bananas, tofu, cats'
    """
    return commator(iterable, ', ', ', ')

def commaand(iterable, lastcomma=', and '):
    """
    Function that takes a iterable and returns a string
    with all the items separated by a comma and a space,
    with and inserted before the last item.

    You can specify a second argument (default = ', and '),
    like commaand(['comma', 'and', 'dot'], ' & ') => 'comma, and & dot'


    """
    return commator(iterable, ', ', str(lastcomma))

# TODO: How to handle nested iterables, v.g. [[1, 2], ['foo', 'bar']]