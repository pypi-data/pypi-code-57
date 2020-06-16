"""
Workflow.Orders>common

Links
`````



"""

from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mangata_workflow_commons',
    version='0.0.9',
    url='http://github.com/pip-services3-python/pip-services3-data-python',
    license='MIT',
    author='Jack Camier, Anastas Fonotov',
    author_email='Jacques.Camier@balfour.com, afonotov@cbi-inet.com',
    description='Data processing and and specific utils modules in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'sqlalchemy', 'cx_oracle', 'pyinstaller', 'requests', 'zeep', 'oauth2', 'pika', 'pysftp', 'pymysql', 'python-dateutil'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ]    
)
 