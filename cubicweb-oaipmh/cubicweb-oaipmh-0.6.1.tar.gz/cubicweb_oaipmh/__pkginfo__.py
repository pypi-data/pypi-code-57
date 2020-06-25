# pylint: disable=W0622
"""cubicweb-oaipmh application packaging information"""


modname = 'cubicweb_oaipmh'
distname = 'cubicweb-oaipmh'

numversion = (0, 6, 1)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'OAI-PMH server for CubicWeb'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb[pyramid]': '>= 3.26.0',
    'six': '>= 1.4.0',
    'python-dateutil': None,
    'isodate': None,
    'pytz': None,
    'lxml': None,
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
