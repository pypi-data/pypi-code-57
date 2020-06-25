from setuptools import setup, find_packages


with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='python-compare-ast',
    version='1.0.0',
    description='Compares ASTs of Python files that have been changed in git',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/omegacen/python-compare-ast",
    license='LGPL-3.0-or-later',
    author='Teake Nutma',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'python-compare-ast = python_compare_ast.__main__:main'
        ]
    },
    python_requires='>=3.6',
    install_requires=[
        'gitpython',
        'click',
        'click-log'
    ]
)
