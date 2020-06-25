import re


class Step(object):

    def __init__(self, path, part, f=None, children=None):
        self.path = path
        self.part = part
        self.f = f
        self.children = children or dict()

    def __contains__(self, item):
        return item in self.children

    def print_tree(self, level=0):
        s = "\t" * level + repr(self) + "\n"
        for child in self.children.values():
            s += child.print_tree(level + 1)
        return s

    def __repr__(self):
        return f"<Step part={self.part} path={self.path} f={self.f}>"


class PathDispatcher(object):
    """PathDispatcher

    Uses a tree to lookup a function by a path. It is tailored to RESTful paths.
    """

    def __init__(self):
        self.registry = Step('/', '/')
        self.regex_paths = list()

    @staticmethod
    def _find(path, step, deepest=False, wildcard=False):
        # if path is empty return step we're at
        if not path:
            return path, step

        # if the next part of the path is not in the step, raise an error
        # optionally can return current step or continue traversing if there is a wilcard node
        if path[0] not in step:
            if deepest:
                return path, step
            elif wildcard and '*' in step:
                return PathDispatcher._find(path[1:], step.children['*'], deepest=deepest, wildcard=wildcard)
            else:
                raise ValueError('Path {} not found in step {}'.format(path, step))
        return PathDispatcher._find(path[1:], step.children[path[0]], deepest=deepest, wildcard=wildcard)

    @staticmethod
    def _insert(full_path, new_path, f, d):
        # find the deepest node that already exists in the tree
        path, deepest_step = PathDispatcher._find(new_path, d, deepest=True)
        if not path and deepest_step.f is not None:
            raise ValueError('Path {} is already registered'.format(new_path))

        # create nodes in the tree for the parts of the path that don't exist
        step = deepest_step
        arg_idx = 0
        while path:
            step = Step(full_path, path[0])

            # if the next step in the path is an optional argument
            # add the function to this step too
            if len(path) > 1 and path[1] == '*':
                if f.args[arg_idx].optional:
                    step.f = f
                arg_idx += 1
            deepest_step.children[path[0]] = step
            deepest_step = step
            path = path[1:]

        # set the function on the last node
        step.f = f

    @staticmethod
    def path_to_parts(path, method):
        if path.startswith('/'):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]
        return [method] + path.split('/')

    def register_rest_function(self, rest_function):
        path = rest_function.path
        if not path.startswith('/'):
            raise ValueError('Must provide full path starting at root /')

        # replace argument parts of the path with a * to represent the wildcard
        arg_regex = re.compile(r'(/\<.*?\>)')
        while arg_regex.search(path):
            path = re.sub(arg_regex, '/*', path, count=1)

        # add the http method as part of the search path
        path_parts = self.path_to_parts(path, rest_function.method)

        self._insert(rest_function.path, path_parts, rest_function, self.registry)
        self.regex_paths.append(rest_function.regex_path)

    def dispatch(self, path, method):
        path_parts = self.path_to_parts(path, method)
        _, step = PathDispatcher._find(path_parts, self.registry, wildcard=True)
        return step.f
