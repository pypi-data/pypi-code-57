import io
import os

from distutils.file_util import copy_file
from setuptools import setup

dir_path = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(dir_path, 'README.rst')
version_path = os.path.join(dir_path, 'VERSION.txt')

with io.open(readme_path, encoding='utf-8') as readme_file:
    readme = readme_file.read()
with io.open(version_path, encoding='utf-8') as version_file:
    version = version_file.read().strip()

base_url = 'https://github.com/sowemail/'

copy_file(version_path,
          os.path.join(dir_path, 'sowerest', 'VERSION.txt'),
          verbose=False)

setup(
    name='sowerest',
    version=version,
    author='Fourat Zouari',
    author_email='fourat@gmail.com',
    url='{}sowerest'.format(base_url),
    download_url='{}sowerest/tarball/{}'.format(base_url, version),
    packages=['sowerest'],
    include_package_data=True,
    license='MIT',
    description='HTTP REST client, simplified for SeWeMail API',
    long_description_content_type='text/x-rst',
    long_description=readme,
    keywords=[
        'REST',
        'HTTP',
        'API',
        'SOWEMAIL'],
    python_requires='>=3.4.*',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
