import os


def get_path_and_all_parents(path):
    '''
    Given a path, yield that path, its parent directory, grandparent directory, and so on, all the
    way up to "/".

    For instance:

        get_path_and_all_parents('/foo/bar/baz')

    ... produces a generator containing:

        ('/foo/bar/baz', '/foo/bar', '/foo', '/')
    '''
    yield path

    if path == '/':
        return

    (parent_path, _) = os.path.split(path)

    yield from get_path_and_all_parents(parent_path)
