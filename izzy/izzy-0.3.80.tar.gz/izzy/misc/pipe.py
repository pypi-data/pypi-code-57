"""

"""

def pipe(*args, intermediates=True):
    """

    Parameters
    ----------
    args
    intermediates

    Returns
    -------

    """

    # Get the length of args and its first record
    num_args = len(args)
    obj = args[0]

    # Sanity check
    assert num_args >= 1, 'must be at least 1 argument'
    assert isinstance(obj, object), 'first argument must be an object'

    #
    obj = args[0]
    for i in range(1, num_args):
        obj.args[i]

