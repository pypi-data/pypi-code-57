

def get_bucket_urn(urn: str) -> str:
    data = urn.split(":", 2)
    return data[0]


def get_file_name_urn(urn: str) -> str:
    data = urn.split(":", 2)
    return data[1]
