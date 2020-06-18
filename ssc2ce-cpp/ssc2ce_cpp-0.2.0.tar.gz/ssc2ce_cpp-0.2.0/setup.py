import os
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion
from distutils.util import get_platform
from wheel.bdist_wheel import bdist_wheel as bdist_wheel_


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

class bdist_wheel(bdist_wheel_):
    def finalize_options(self):
        from sys import platform as _platform
        platform_name = get_platform()
        if _platform == "linux" or _platform == "linux2":
            # Linux
            platform_name = 'manylinux1_x86_64'

        bdist_wheel_.finalize_options(self)
        self.universal = True
        self.plat_name_supplied = True
        self.plat_name = platform_name

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ssc2ce_cpp',
    version='0.2.0',
    author='Oleg Nedbaylo',
    author_email='olned64@gmail.com',
    description='A set of C++ parsers for ssc2ce',
    long_description=long_description,
    ext_modules=[CMakeExtension('ssc2ce_cpp')],
    cmdclass=dict(build_ext=CMakeBuild, bdist_wheel=bdist_wheel),
    test_suite='tests',
    # tests_require=['pytest'],
    zip_safe=False,
)
