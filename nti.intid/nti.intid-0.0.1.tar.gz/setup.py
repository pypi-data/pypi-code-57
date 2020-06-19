import codecs
from setuptools import setup
from setuptools import find_packages

entry_points = {
    'console_scripts': [
    ],
}

TESTS_REQUIRE = [
    'coverage',
    'ZODB',
    'fudge',
    'nti.site',
    'nti.testing',
    'persistent',
    'transaction',
    'zope.dottedname',
    'zope.site',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.intid',
    version='0.0.1',
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="Extensions for Zope3's intids.",
    long_description=(
        _read('README.rst')
        + '\n\n'
        + _read("CHANGES.rst")
    ),
    license='Apache',
    keywords='intid zope3',
    classifiers=[
        'Framework :: Zope3',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    url="https://github.com/NextThought/nti.intid",
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'Acquisition',
        'BTrees',
        'nti.externalization',
        'nti.ntiids',
        'nti.wref',
        'setuptools',
        'zc.intid',
        'zope.component',
        'zope.deferredimport',
        'zope.deprecation',
        'zope.event',
        'zope.interface',
        'zope.intid',
        'zope.keyreference',
        'zope.location',
        'zope.security',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
            'Sphinx',
            'repoze.sphinx.autointerface',
            'sphinx_rtd_theme',
        ],
    },
    entry_points=entry_points,
)
