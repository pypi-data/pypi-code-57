# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filediffs', 'filediffs.tests']

package_data = \
{'': ['*'], 'filediffs.tests': ['data/*']}

install_requires = \
['cython==0.29.19']

entry_points = \
{'console_scripts': ['my-script = separatefiles:separate_files_script']}

setup_kwargs = {
    'name': 'filediffs',
    'version': '0.0.2',
    'description': 'Separate two file into lines observed in both-/first_only-/second_only. Programmed using Cython.',
    'long_description': "# The filediffs package\n`filediffs` takes two files and separates them into \n1. lines found in both files\n2. lines found only in file 1\n3. lines found only in file 2\n\nCode inspired by https://www.splinter.com.au/reconcilingcomparing-huge-data-sets-with-c/\n\n# Installation\nFor package installation, [Poetry](https://python-poetry.org/) is used.\n\nInside pyproject.toml the python version, requirements,\nbuild instructions, package descriptions etc. are defined.\n\nYou can create a virtual environment for the package with\npoetry by \n1. installing poetry `pip install poetry`\n2. calling `poetry install` to install from poetry.lock\n\nTo create a .tar.gz file and wheeles for publishing the package one can use `poetry build`\n\nTo publish the package, `poetry publish` can be used. Though \nthe pipy credentials have to be set (see https://python-poetry.org/docs/repositories/#configuring-credentials).\n\n# Implementation:\nImplemented in Cython.\n\nLines found in both files are not kept in memory but written to\n disk every 5.000.000 lines to preserve memory. \n \nThis way, even very large files can be separated.\nOnly the diff has to fit in memory.\n\nThe file `build_cython_setup.py` defines the cython build process.\n The cpp files can be build using `python build_cython_setup.py build_ext --inplace`.\n \n # Usage:\nTo use the method in python in interaction with cython,\nthe file paths have to passed to the function as bytestrings.\n```python\nfrom filediffs.filediffs import file_diffs\nlines_only_in_file_1, lines_only_in_file_2 = file_diffs(\n    filename_1=b'path/to/file1.txt',\n    filename_2=b'path/to/file2.txt',\n    outpath_lines_present_in_both_files=b'output_path/to/lines_in_both.txt',\n    outpath_lines_present_only_in_file1=b'output_path/to/lines_only_in_file1.txt',\n    outpath_lines_present_only_in_file2=b'output_path/to/lines_only_in_file2.txt',\n)\n```\n\nInside the package directory, an example script `filediffs_script.py` is provided.\n\nIt can be used to separate files from the terminal:\n```\n# To separate two files, simply pass the filepath to `filediffs/filediffs_script.py`\npython filediffs/filediffs_script.py filediffs/tests/data/file_1.txt filediffs/tests/data/file_2.txt\n\n# If you want to define the filenames of the separated files, optional arguments are provided for the script. \npython filediffs/filediffs_script.py filediffs/tests/data/file_1.txt filediffs/tests/data/file_2.txt --out_filename_both out_both.txt --out_filename_only_in_file1 out_file1_only.txt --out_filename_only_in_file2 out_file2_only.txt\n```\n\n\n",
    'author': 'Sebastian Cattes',
    'author_email': 'sebastian.cattes@inwt-statistics.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
