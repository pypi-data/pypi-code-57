

def get_cached_value(holder_object, cache_key, getter, *args, **kwargs):
    if not hasattr(holder_object, cache_key):
        setattr(holder_object, cache_key, getter(*args, **kwargs))
    return getattr(holder_object, cache_key)
