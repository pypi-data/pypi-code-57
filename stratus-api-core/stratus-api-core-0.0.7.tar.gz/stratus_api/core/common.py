def chunkify(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def generate_random_id():
    """Generate a random id

    :return: a unique UUID4 formatted string
    """
    import uuid
    return str(uuid.uuid4())


def generate_hash_id(data):
    import json
    import uuid
    import hashlib
    hash_id = uuid.UUID(
        hashlib.md5(
            str(json.dumps(data, sort_keys=True)).encode('utf-8')
        ).hexdigest()
    )
    return str(hash_id)
