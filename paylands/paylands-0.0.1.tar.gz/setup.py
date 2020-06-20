import os

from setuptools import find_packages, setup


def read(*parts):
    with open(os.path.join(*parts), 'r') as f:
        return f.read()


def find_version(*file_paths):
    _locals = locals()
    exec(read(*file_paths), globals(), _locals)
    if '__version__' not in _locals:
        raise RuntimeError('Unable to find version string.')
    return _locals['__version__']


def install_requires():
    return read('requirements.txt')


def tests_require():
    return read('dev-requirements.txt')


setup(
    name='paylands',
    version=find_version('paylands', 'version.py'),
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=install_requires(),
    tests_require=tests_require(),
    description='Paylands API client',
    url='https://github.com/menudoproblema/paylands',
    author='Granada Dynamics, SL',
    license='MIT License',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    zip_safe=True,
)
