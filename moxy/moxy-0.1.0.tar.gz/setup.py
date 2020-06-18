import os
import re
import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader

from setuptools import setup

DIR = Path(__file__).resolve().parent
url = "https://github.com/blakev/moxy"
description = "Pythonic interface for storing runtime metrics."
long_description = (DIR / 'README.md').read_text()
version = SourceFileLoader('version', 'moxy/version.py').load_module()

# generate extra docs
try:
    history = (DIR / 'HISTORY.md').read_text()
    history = re.sub(r'#(\d+)', f'[#\1]({url}/issues/\1)', history)
    history = re.sub(r'( +)@([\w\-]+)', r'\1[@\2](https://github.com/\2)', history, flags=re.I)
    history = re.sub('@@', '@', history)

    long_description = f'{long_description}\n\n{history}'
except FileNotFoundError:
    long_description = f'{long_description}\n\nSee {url} for more information.'

# compile
ext_modules = None
if not any(arg in sys.argv for arg in ['clean', 'check']) and 'SKIP_CYTHON' not in os.environ:
    try:
        from Cython.Build import cythonize
    except ImportError:
        pass
    else:
        # For cython test coverage install with `make build-cython-trace`
        compiler_directives = {}
        if 'CYTHON_TRACE' in sys.argv:
            compiler_directives['linetrace'] = True
        os.environ['CFLAGS'] = '-O3'
        ext_modules = cythonize(
            'moxy/*.py',
            exclude=[],
            nthreads=int(os.getenv('CYTHON_NTHREADS', 0)),
            language_level=3,
            compiler_directives=compiler_directives,
        )
# ~~
setup(
    name='moxy',
    version=str(version.version_str),
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
    ],
    author='Blake VandeMerwe',
    author_email='blakev@null.net',
    url=url,
    license='GPLv3',
    packages=['moxy'],
    package_data={'moxy': ['py.typed']},
    python_requires='>=3.8',
    zip_safe=False,
    use_pipfile={
        'path': 'Pipfile',
        'interpolate': False,
        'pythons': False,
    },
    ext_modules=ext_modules,
)
