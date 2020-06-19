from pprint import pprint

import functools


def traceback_function(func):
    @functools.wraps(func)
    def _decorator(*args, **kwargs):
        type_arg = {}
        type_kwarg = {}
        if args:
            for arg in args:
                if arg in type_arg:
                    type_arg['*' + str(arg)] = {arg: type(arg)}
                else:
                    type_arg[arg] = type(arg)
        if kwargs:
            for kwarg in kwargs:
                type_kwarg[kwarg] = type(kwarg)
        if 'dirs' in kwargs and kwargs['dirs']:
            for arg in args:
                pprint(f'{arg} - {dir(arg)}')
            for kwarg in kwargs:
                pprint(f'{kwarg} - {dir(kwarg)}')

        print(f'Trace: {func.__name__}() function is called with args: {type_arg}, kwargs: {type_kwarg}')
        result = func(*args, **kwargs)
        print(f'Trace: {func.__name__}() return: "{result}"')
        return result
    return _decorator


if __name__ == '__main__':
    @traceback_function
    def my_ff(name, age, job, dirs):
        """My Function"""
        return f'Name: {name}, Age: {age}, Job: {job}'


    my_ff('Vlad', 23, True, dirs=True)


    @traceback_function
    def new():
        """test"""
        news = 5


    print(new())
    # print(new(x=5, y=5))
