import re


class PathArg(object):
    __slots__ = ('type_', 'name', 'optional')

    def __init__(self, type_, name, optional=None):
        self.type_ = eval(type_)
        self.name = name
        self.optional = optional is not None

    def parse(self, val):
        if val is None:
            return val
        return self.type_(val)

    def __eq__(self, other):
        return (self.type_ == other.type_
                and self.name == other.name
                and self.optional == other.optional)


class RestFunction(object):
    """Wrapper class for a restful function to store metadata."""
    ARG_REGEX = '[A-Za-z0-9_-]'

    def __init__(self, f, path, method, response_type='json'):
        self.f = f
        self.path = path
        self.method = method
        self.args = self.args_from_path(self.path)
        self.regex_path = self.path_to_regex_path(self.args, self.path)
        self.response_type = response_type

    @staticmethod
    def args_from_path(path):
        """Strip arguments from path and create parser."""
        args = [PathArg(*arg.split(':')) for arg in re.findall(r'\<(.*?)\>', path)]
        if len(args) > 1:
            assert not any(arg.optional for arg in args[:-1]), "Cannot have an optional uri argument followed by more arguments"
        return args

    @staticmethod
    def path_to_regex_path(args, path):
        """Convert restful path format to tornado regex format."""
        for arg in args:
            r = '/({}+)'.format(RestFunction.ARG_REGEX)
            if arg.optional:
                r = '(?:/?$|/)({}+)?'.format(RestFunction.ARG_REGEX)
            path = re.sub(r'(/\<.*?\>)', r, path, count=1)
        path += '/?'
        return path

    def __call__(self, handler, *args):
        args = dict([(parser.name, parser.parse(val)) for parser, val in zip(self.args, args)])
        return self.f(handler, **args)