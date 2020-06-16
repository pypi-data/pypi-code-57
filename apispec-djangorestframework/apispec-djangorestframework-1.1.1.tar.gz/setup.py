import os
from distutils.core import setup

from setuptools import find_packages

exec(compile(open(os.path.join(os.path.dirname(__file__), 'apispec_drf/version.py'), "rb").read(), os.path.join(os.path.dirname(__file__), 'apispec_drf/version.py'), 'exec'))


setup(
    name='apispec-djangorestframework',
    version=".".join(map(str, VERSION)),
    packages=find_packages(),
    include_package_data=True,

    author='Concentric Sky',
    author_email='django@concentricsky.com',
    description='DjangoRestFramework 3.6.x APISpec generator',
    license='Apache2'
)
