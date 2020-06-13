def shorten_func(func_name, *args_global, **kwargs_global):
    """
    Reduce to pass the same parameters multiple times when calling a function multiple times
    Example:
        before:
            first_name = get_json_object_by_path(object_passed_repeatedly, '/event/0/person/first_name', '')
            last_name = get_json_object_by_path(object_passed_repeatedly, '/event/0/person/last_name', '')
        after:
            get = shorten_func(get_json_object_by_path, object_passed_repeatedly, default='')
            first_name = get('/event/0/person/first_name')
            last_name = get('/event/0/person/last_name')

    :param func_name: the function name
    :param args_global: arguments passed repeatedly
    :return: The same function but it requires fewer parameters
    """
    return lambda *args_local: func_name(*args_global, *args_local, **kwargs_global)
