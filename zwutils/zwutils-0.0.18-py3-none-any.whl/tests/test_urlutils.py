import pytest

from zwutils.urlutils import *

def test_urlutils():
    d = ('http://a.com/b?p1=1&p2=2', 'http://a.com/b')
    assert remove_args(d[0]) == d[1]

    d = ('http://a.com/b?url=http%3A%2F%2Fr.com', 'http://r.com')
    assert get_redirect(d[0]) == d[1]

    d = ('http://a.com/b', 'a.com')
    assert get_domain(d[0]) == d[1]

    d = ('http://a.com/b', 'http')
    assert get_scheme(d[0]) == d[1]

    d = ('http://a.com/b/c?p1=1', '/b/c')
    assert get_path(d[0]) == d[1]

    d = ('http://a.com/b/c?p1=1', True)
    assert is_abs_url(d[0]) == d[1]
    d = ('b/c?p1=1', False)
    assert is_abs_url(d[0]) == d[1]

    d = ('http://blahblah/images/car.jpg', 'jpg')
    assert url_to_filetype(d[0]) == d[1]

    d = ('http://a.com/b/c?p1=1', 'http://a.com')
    assert get_base(d[0]) == d[1]