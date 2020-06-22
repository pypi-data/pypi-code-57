import warnings


def deprecated_api(prefer, hint="This API is deprecated please using prefer one."):
    msg = "{}. Prefer: {}.".format(hint, prefer)

    def decorator(func):
        warnings.warn(msg, DeprecationWarning)

        def decorated(*args, **kwargs):
            return func(*args, **kwargs)

        return decorated

    return decorator


if __name__ == "__main__":
    @deprecated_api(deprecated_api)
    def print_hello():
        print("hello")

    print_hello()
