import warnings


def deprecated_support(hint="This API is deprecated please using prefer one."):
    msg = "{}. ".format(hint)

    def decorator(func):
        warnings.warn(msg, DeprecationWarning)

        def decorated(*args, **kwargs):
            return func(*args, **kwargs)

        return decorated

    return decorator


if __name__ == "__main__":
    @deprecated_support()
    def print_hello():
        print("hello")

    print_hello()
