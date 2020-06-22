"""
   SDC decorators module
"""
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError


def query_exception_handler(exceptions: tuple = (SQLAlchemyError, )):
    """
        Decorator - handling SqlAlchemy specific exceptions

        args:
            exceptions (Exception): List of exceptions to catch

        return:
            Wrapped function's response
    """
    def query_exception_decorator(function):
        @wraps(function)
        def func_with_exceptions(*args, **kwargs):
            """
                Wrapper function to decorate function with
            """
            try:
                return function(*args, **kwargs)
            except exceptions as ex:
                raise Exception(
                    'Server Error: {ex}'.format(
                        ex=str(ex.__dict__['orig'])
                    )
                )

        return func_with_exceptions

    return query_exception_decorator
