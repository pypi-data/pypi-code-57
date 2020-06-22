# type: ignore
from setuptools import setup, find_packages


def readfile(name):
    with open(name) as f:
        return f.read()


readme = readfile('README.rst')
changes = readfile('CHANGES.rst')

requires = [
    'htm',
    'MarkupSafe',
    'typing_extensions>=3.7.4;python_version<"3.8"'
]

docs_require = [
    'Sphinx',
    'sphinx-book-theme',
    'myst-parser'
]

tests_require = [
    'pytest',
    'pytest-mock',
    'pytest-cov',
    'mypy',
    'pytest-mypy',
    'py',
    'coverage',
    'tox',
    'black',
    'flake8',
]

setup(
    name='viewdom',
    description=(
        'View layer for Python VDOMs'
    ),
    version='0.4.0',
    long_description=readme + '\n\n' + changes,
    long_description_content_type='text/x-rst',
    author='Paul Everitt',
    author_email='pauleveritt@me.com',
    url='https://viewdom.readthedocs.io',
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    package_data={"viewdom": ["py.typed"]},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=requires,
    extras_require={'docs': docs_require, 'tests': tests_require},
    zip_safe=False,
    keywords=','.join(
        [
            'web',
            'html',
            'components',
            'templates',
        ]
    ),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
