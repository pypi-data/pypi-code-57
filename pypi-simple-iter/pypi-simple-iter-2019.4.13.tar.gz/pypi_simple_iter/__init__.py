__all__ = ['iter_projects_from_file']

import os
import tempfile
from tempfile import mkstemp, mkdtemp

import pypi_slug
import requests_retry_on_exceptions as requests

def iter_projects_from_file(path):
    with open(path) as f:
        for l in f:
            if 'href' in l:
                name = l.split('>')[1].split('<')[0]
                slug = pypi_slug.getslug(name)
                yield slug, name

def iter_projects(url=None):
    f, path = tempfile.mkstemp()
    os.close(f)
    try:
        r = requests.get(url if url else 'https://pypi.org/simple/')
        open(path,'w').write(r.text)
        for slug,name in iter_projects_from_file(path):
            yield slug, name
    finally:
        os.unlink(path)


