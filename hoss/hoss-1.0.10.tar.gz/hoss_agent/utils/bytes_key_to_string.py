
# helper to check if dictionary key is bytes and if so decode them into string, recursively
def bytes_key_to_string(d):
    rval = {}
    if not isinstance(d, dict):
        if isinstance(d, (tuple, list, set)):
            v = [bytes_key_to_string(x) for x in d]
            return v
        else:
            return d
    for k, v in d.items():
        if isinstance(k, bytes):
            k = k.decode()
        if isinstance(v, dict):
            v = bytes_key_to_string(v)
        elif isinstance(v, (tuple, list, set)):
            v = [bytes_key_to_string(x) for x in v]
        rval[k] = v
    return rval
