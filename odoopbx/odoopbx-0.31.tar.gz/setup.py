'''
Odoo PBX management application.
'''
import atexit
from setuptools import setup
from setuptools.command.install import install
import os
from os.path import abspath, dirname, join


def get_version():
    try:
        version_file = open(
            os.path.join(
                os.path.dirname(__file__), 'VERSION.txt')
        ).readlines()[0].strip()
        return version_file
    except Exception:
        raise RuntimeError('Unable to find version string.')


def read_file(filename):
    '''Read the contents of a file located relative to setup.py'''
    with open(join(abspath(dirname(__file__)), filename)) as thefile:
        return thefile.read()


def odoopbx_post_install():
    try:
        from site import getsitepackages
        site_packages = getsitepackages()[0]
    except (ImportError, Exception):
        from distutils.sysconfig import get_python_lib
        site_packages = get_python_lib()
    base_dir = os.path.join(site_packages, 'odoopbx')
    path_conf_tmpl = """file_roots:
  base:
    - {}
pillar_roots:
  base:
    - {}
extension_modules: {}
"""
    conf = path_conf_tmpl.format(
        os.path.join(base_dir, 'salt', 'roots'),
        os.path.join(base_dir, 'salt', 'pillar'),
        os.path.join(base_dir, 'salt', 'extensions'),
    )
    open(os.path.join(
        base_dir, 'salt', 'minion.d', '_path.conf'), 'w').write(conf)


class odoopbx_install(install):

    def run(self, *args, **kwargs):
        super(odoopbx_install, self).run(*args, **kwargs)
        self.execute(odoopbx_post_install, ())

setup(
    author='Odooist',
    author_email='odooist@gmail.com',
    license='Odoo Enterprise Edition License v1.0',
    name='odoopbx',
    version=get_version(),
    description=__doc__.strip(),
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/odoopbx',
    cmdclass={'install': odoopbx_install},
    package_dir={'odoopbx': ''},
    packages=[
        'odoopbx.salt',
        'odoopbx.scripts',
    ],
    include_package_data=True,
    package_data={
        'odoopbx.salt': [
            'extensions',
            'master.d',
            'minion.d',
            'pillar',
            'roots',
        ],
    },
    install_requires=[
        'salt',
        'click',
        'tornado-httpclient-session',
    ],
    entry_points='''
[console_scripts]
odoopbx=odoopbx.scripts.odoopbx_cli:main
    ''',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
