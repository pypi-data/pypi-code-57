
SETUP_INFO = dict(
    name = 'infi.dygraphs',
    version = '0.14',
    author = 'Itay Galea',
    author_email = 'igalea@infinidat.com',

    url = 'https://git.infinidat.com/host-internal/infi.dygraphs',
    license = 'BSD',
    description = """A fork of http://dygraphs.com/ with INFINIDAT-specific customizations and utilities.""",
    long_description = """A fork of http://dygraphs.com/ with INFINIDAT-specific customizations and utilities.""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = ['setuptools'],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': [
'*.css',
'*.html',
'*.js'
]},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

