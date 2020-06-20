from pathlib import Path

from Cython.Build import cythonize
from Cython.Distutils.build_ext import new_build_ext
from setuptools import Extension, setup

setup(
    name='testcython',
    version='0.0.1',
    description='pypi test for cython package',
    author='test cython',
    author_email='test@cython.com',
    license='MIT',
    requires=['cython'],
    package_data={'testcython': [str(Path(__file__).parent / 'testcython' / "cythonize_me.pyx")]},
    extensions=[Extension("testcython", [str(Path(__file__).parent / 'testcython' / "cythonize_me.pyx")])],
    ext_modules=cythonize(Extension("testcython", [str(Path(__file__).parent / 'testcython' / "cythonize_me.pyx")])),
    cmdclass={'build_ext': new_build_ext},
)
