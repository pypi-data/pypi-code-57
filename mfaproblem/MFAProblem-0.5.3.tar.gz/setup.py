from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import setuptools.command.sdist
import setuptools.command.install
import setuptools.command.egg_info
import wheel.bdist_wheel

import shutil
import setuptools
import sys
import os


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


def get_eigen_include():
    if 'EIGEN_INCLUDE' in os.environ:
        return os.environ['EIGEN_INCLUDE']
    else:
        return 'mfa_problem_matrices/include/eigen'


ext_modules = [
    Extension(
        'mfa_problem_matrices',
        ['mfa_problem_matrices/src/main.cpp'],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
            get_eigen_include()
        ],
        language='c++'
    ),
]


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.

    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support '
                           'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            # opts.append('-fopenmp')
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
            # opts.append('-fopenmp')
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


def get_long_description():
    try:
        with open('mfa_problem/README.rst') as f:
            long_description = f.read()
            return long_description
    except Exception:
        with open('README.rst') as f:
            long_description = f.read()
            return long_description


class BuildPyCommand(setuptools.command.sdist.sdist):
    """Custom build command."""
    def run(self):
        build_py = self.get_finalized_command('build_py')
        mfa_problem_dir = build_py.get_package_dir('mfa_problem')
        root_dir = os.path.dirname(mfa_problem_dir)
        #shutil.copyfile(os.path.join(root_dir, 'requirements.txt'), os.path.join(mfa_problem_dir, 'requirements.txt'))
        test_dir = os.path.join(root_dir, 'tests')
        cp_test_dir = os.path.join(mfa_problem_dir, 'tests')
        if not os.path.exists(cp_test_dir):
            shutil.copytree(test_dir, cp_test_dir)
        data_dir = os.path.join(root_dir, 'data/input')
        cp_data_dir = os.path.join(mfa_problem_dir, 'data')
        if not os.path.exists(cp_data_dir):
            shutil.copytree(data_dir, cp_data_dir)
        super(BuildPyCommand, self).run()
        # shutil.rmtree(cp_test_dir)
        # shutil.rmtree(cp_data_dir)


class InstallPyCommand(setuptools.command.install.install):
    """Custom build command."""
    def run(self):
        build_py = self.get_finalized_command('build_py')
        mfa_problem_dir = build_py.get_package_dir('mfa_problem')
        root_dir = os.path.dirname(mfa_problem_dir)
        #shutil.copyfile(os.path.join(root_dir, 'requirements.txt'), os.path.join(mfa_problem_dir, 'requirements.txt'))
        test_dir = os.path.join(root_dir, 'tests')
        cp_test_dir = os.path.join(mfa_problem_dir, 'tests')
        if not os.path.exists(cp_test_dir):
            shutil.copytree(test_dir, cp_test_dir)
        data_dir = os.path.join(root_dir, 'data/input')
        cp_data_dir = os.path.join(mfa_problem_dir, 'data')
        if not os.path.exists(cp_data_dir):
            shutil.copytree(data_dir, cp_data_dir)
        super(InstallPyCommand, self).run()
        # shutil.rmtree(cp_test_dir)
        # shutil.rmtree(cp_data_dir)


class EggInfoPyCommand(setuptools.command.egg_info.egg_info):
    """Custom build command."""
    def run(self):
        build_py = self.get_finalized_command('build_py')
        mfa_problem_dir = build_py.get_package_dir('mfa_problem')
        root_dir = os.path.dirname(mfa_problem_dir)
        #shutil.copyfile(os.path.join(root_dir, 'requirements.txt'), os.path.join(mfa_problem_dir, 'requirements.txt'))
        test_dir = os.path.join(root_dir, 'tests')
        cp_test_dir = os.path.join(mfa_problem_dir, 'tests')
        if not os.path.exists(cp_test_dir):
            shutil.copytree(test_dir, cp_test_dir)
        data_dir = os.path.join(root_dir, 'data/input')
        cp_data_dir = os.path.join(mfa_problem_dir, 'data')
        if not os.path.exists(cp_data_dir):
            shutil.copytree(data_dir, cp_data_dir)
        super(EggInfoPyCommand, self).run()
        # shutil.rmtree(cp_test_dir)
        # shutil.rmtree(cp_data_dir)


class BDistWheelInfoPyCommand(wheel.bdist_wheel.bdist_wheel):
    """Custom build command."""
    def run(self):
        build_py = self.get_finalized_command('build_py')
        mfa_problem_dir = build_py.get_package_dir('mfa_problem')
        root_dir = os.path.dirname(mfa_problem_dir)
        #shutil.copyfile(os.path.join(root_dir, 'requirements.txt'), os.path.join(mfa_problem_dir, 'requirements.txt'))
        test_dir = os.path.join(root_dir, 'tests')
        cp_test_dir = os.path.join(mfa_problem_dir, 'tests')
        if not os.path.exists(cp_test_dir):
            shutil.copytree(test_dir, cp_test_dir)
        data_dir = os.path.join(root_dir, 'data/input')
        cp_data_dir = os.path.join(mfa_problem_dir, 'data')
        if not os.path.exists(cp_data_dir):
            shutil.copytree(data_dir, cp_data_dir)
        super(BDistWheelInfoPyCommand, self).run()
        # shutil.rmtree(cp_test_dir)
        # shutil.rmtree(cp_data_dir)


setup(
    name='MFAProblem',
    version='0.5.3',
    description='Material Flow Analysis Problem',
    url='https://gitlab.com/su-model/mfa_problem',
    author='AFM Filieres',
    author_email='julien.alapetite@gmail.com',
    test_suite='tests',
    scripts=[
        'bin/install_mfa_problem_notebook.py',
        'bin/run_mfa_problem_main_with_excel.py',
        'bin/run_create_empty_ter.py',
        'bin/run_import_excel_data_in_data_base.py',
        'bin/run_import_excel_proxy_in_data_base.py',
        'bin/run_mfa_problem_check_input.py',
        'bin/run_proxycalc.py'
    ],
    packages=['mfa_problem', 'mfa_problem.tests.integration', 'mfa_problem.tests.unit'],
    package_dir={'mfa_problem': 'mfa_problem'},
    package_data={'mfa_problem': ['data/*.*']},
    ext_modules=ext_modules,
    install_requires=[
        'openpyxl',
        'pandas',
        'sympy',
        'cvxpy',
        'argparse',
        'pybind11',
        'xmltodict',
        'psutil',
        'sqlalchemy',
        'xlrd',
        'parameterized',
        'numpy',
    ],
    cmdclass={
        'build_ext': BuildExt,
        'sdist': BuildPyCommand,
        'install': InstallPyCommand,
        'egg_info': EggInfoPyCommand,
        'bdist_wheel': BDistWheelInfoPyCommand
    },
    long_description=get_long_description(),
    long_description_content_type='text/x-rst'
)

# Command to run
# python setup.py sdist bdist_wheel
# python -m twine upload -u julien.alapetite -p Hourgada$1 --repository pypi dist/*
