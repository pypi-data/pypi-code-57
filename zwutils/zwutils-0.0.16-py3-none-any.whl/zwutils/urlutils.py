
import re
from urllib.parse import parse_qs, urljoin, urlparse, urlsplit, urlunsplit

def remove_args(url, keep_params=(), frags=False):
    """
    Remove all param arguments from a url.
    """
    parsed = urlsplit(url)
    filtered_query = '&'.join(
        qry_item for qry_item in parsed.query.split('&')
        if qry_item.startswith(keep_params)
    )
    if frags:
        frag = parsed[4:]
    else:
        frag = ('',)
    return urlunsplit(parsed[:3] + (filtered_query,) + frag)

def get_redirect(url, param_name='url'):
    """Get redirect url from url with given param name('url' default)
    """
    parse_data = urlparse(url)
    query = parse_data.query

    query_item = parse_qs(query)
    if query_item.get(param_name):
        return query_item[param_name][0]
    return url

def get_domain(abs_url, **kwargs):
    """
    returns a url's domain
    """
    if abs_url is None:
        return None
    return urlparse(abs_url, **kwargs).netloc

def get_scheme(abs_url, **kwargs):
    """
    """
    if abs_url is None:
        return None
    return urlparse(abs_url, **kwargs).scheme

def get_path(abs_url, **kwargs):
    """
    """
    if abs_url is None:
        return None
    return urlparse(abs_url, **kwargs).path

def get_base(abs_url, **kwargs):
    return '%s://%s' % ( get_scheme(abs_url, **kwargs),get_domain(abs_url, **kwargs) )

def is_abs_url(url):
    """
    this regex was brought to you by django!
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'                                                                 # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'                                                                         # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'                                                # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'                                                        # ...or ipv6
        r'(?::\d+)?'                                                                          # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    c_regex = re.compile(regex)
    return (c_regex.search(url) is not None)

def url_to_filetype(abs_url):
    """
    Input a URL and output the filetype of the file
    specified by the url. Returns None for no filetype.
    'http://blahblah/images/car.jpg' -> 'jpg'
    'http://yahoo.com'               -> None
    """
    path = urlparse(abs_url).path
    # Eliminate the trailing '/', we are extracting the file
    if path.endswith('/'):
        path = path[:-1]
    path_chunks = [x for x in path.split('/') if len(x) > 0]
    if len(path_chunks) == 0:
        # 'http://yahoo.com'
        return None
    last_chunk = path_chunks[-1].split('.')  # last chunk == file usually
    if len(last_chunk) < 2:
        return None
    file_type = last_chunk[-1]
    # Assume that file extension is maximum 5 characters long
    if len(file_type) <= 5:
        return file_type.lower()
    return None
