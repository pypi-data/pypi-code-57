import sys
from distutils.core import setup


def get_version(filename):
    import ast
    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith('__version__'):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError('No version found in %r.' % filename)
    if version is None:
        raise ValueError(filename)
    return version


if sys.version_info < (3, 5):
    msg = 'flat-dict works with Python 3.5 and later.\nDetected %s.' % str(sys.version)
    sys.exit(msg)

lib_version = get_version(filename='flat_dict/__init__.py')

setup(
    name='flat-dict',
    packages=[
        'flat_dict'
    ],
    version=lib_version,
    license='MIT',
    description='Transform nested Python dictionaries into flat (key, value) sets, and back',
    author='Andrea F. Daniele',
    author_email='afdaniele@ttic.edu',
    url='https://github.com/afdaniele/',
    download_url='https://github.com/afdaniele/flat-dict/tarball/{}'.format(lib_version),
    zip_safe=False,
    include_package_data=True,
    keywords=['flat', 'dict', 'list', 'dict', 'x-www-form-urlencoded'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
