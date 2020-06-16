# -*- coding: utf-8 -*-
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
###############################################################################
from distutils.core import setup
from setuptools import find_packages
import os
import shutil
from pathlib import Path

this = os.path.dirname(__file__)
with open(os.path.join(this, "requirements.txt"), "r") as f:
    requirements = [_ for _ in [_.strip("\r\n ")
                                for _ in f.readlines()] if _ is not None]

tool_folder = 'onnxruntime_tools'


def build_pkg_folder(root_dir):
    dist_dir = Path(root_dir) / tool_folder
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    ignore = shutil.ignore_patterns('test_*.py')
    shutil.copytree(Path(root_dir)
                    / 'runtime' / 'onnxruntime' / 'onnxruntime' / 'python' / 'tools', dist_dir,
                    ignore=ignore)
    shutil.copyfile(Path(root_dir) / 'pkg_init.py_', dist_dir / '__init__.py')
    shutil.copyfile(Path(root_dir) / 'optimizer.py_', dist_dir / 'optimizer_cli.py')
    Path.touch(dist_dir / 'transformers' / '__init__.py')

    # remove unnecessary files
    exclude_files = [ dist_dir / 'onnxruntime_test.py',
                      dist_dir / 'transformers' / 'test_optimizer.py',
                      dist_dir / 'transformers' / 'benchmark_gpt2.py',
                      dist_dir / 'transformers' / 'ShapeOptimizer.py',
                    ]

    for file in exclude_files:
        if file.exists():
            os.remove(file)

def read_version(root_dir, package):
    # read version from the package file.
    version_str = '0.0.1.0000'
    init_file = Path(root_dir) / package / '__init__.py'
    with (open(init_file, "r")) as f:
        line = [_ for _ in [_.strip("\r\n ")
                            for _ in f.readlines()] if _.startswith("__version__")]
        if len(line) > 0:
            version_str = line[0].split('=')[1].strip('" ')
    return version_str


def read_long_description(root_dir, package):
    readme_path = Path(root_dir) / package / 'transformers' / 'README.md'
    with open(readme_path, encoding='utf-8') as f:
        description = f.read()
        start_pos = description.find('# Introduction')
        if start_pos >= 0:
            description = description[start_pos:]

    return description


build_pkg_folder(this)
packages = find_packages()
assert packages, 'Cannot find a package in the directory' + this
root_package = packages[0]
version_str = read_version(this, root_package)
long_description = read_long_description(this, root_package)

setup(
    name=root_package,
    version=version_str,
    description="Transformers Model Optimization Tool of ONNXRuntime",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    author='Microsoft Corporation',
    author_email='onnx@microsoft.com',
    url='https://github.com/microsoft/onnxruntime',
    packages=packages,
    include_package_data=True,
    install_requires=requirements,
    tests_require=['pytest', 'pytest-cov'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License']
)
