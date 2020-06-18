def deprecated(reason: str):
    def state_deprecated(f):
        def new_f(*args, **kwargs):
            print("Warning: {} is deprecated: {}".format(f.__name__, reason))
            return f(*args, **kwargs)

        return new_f

    return state_deprecated
