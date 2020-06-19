from functools import wraps

from .local_files import destroy_all_static_files


def static_changer(cls):
    """
    Model decorator, add to models that will change static pages
    """
    def destroy_wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            destroy_all_static_files()
            return f(*args, **kwargs)
        return inner

    # Scorched earth - since we can't know what static file gets affected,
    # just delete all of them
    cls.save = destroy_wrapper(cls.save)
    cls.delete = destroy_wrapper(cls.delete)
    return cls
