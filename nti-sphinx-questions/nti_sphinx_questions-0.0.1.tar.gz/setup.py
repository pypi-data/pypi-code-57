import codecs
from setuptools import setup
from setuptools import find_packages

entry_points = {
}

TESTS_REQUIRE = [
    'coverage',
    'zope.testrunner',
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti_sphinx_questions',
    version='0.0.1',
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="Question and Question List Sphinx directives",
    long_description=(
        _read('README.rst')
        + '\n\n'
        + _read("CHANGES.rst")
    ),
    long_description_content_type='text/x-rst',
    license='BSD',
    keywords='sphinx extension question',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Documentation',
        'Topic :: Utilities',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
    ],
    url="https://github.com/NextThought/nti_sphinx_questions",
    zip_safe=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'Sphinx >= 1.8.0',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        'docs': [
        ],
    },
    entry_points=entry_points,
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*",
)
