from deepcrawl.exceptions import InvalidContentType


# Generate request headers with the API connection token and the appropriate content-type
def get_request_headers(token="", content_type='json'):
    if content_type == 'json':
        content_type_value = 'application/json'
    elif content_type == 'form':
        content_type_value = 'application/x-www-form-urlencoded'
    else:
        raise InvalidContentType

    return {
        'X-Auth-Token': token,
        'Content-Type': content_type_value,
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip, deflate'
    }
