import io
from os import path

from setuptools import setup

version = {}
with open('osecore/version.py') as fp:
    exec(fp.read(), version)

current_dir = path.abspath(path.dirname(__file__))
with io.open(path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ose-workbench-core',
    version=version['__version__'],
    packages=[
        'osecore',
        'osecore.app',
        'osecore.app.attachment',
        'osecore.app.cut_list',
        'osecore.app.shape',
        'osecore.app.shape.edge',
        'osecore.app.shape.face',
        'osecore.gui',
        'osecore.gui.cut_list',
        'osecore.gui.selection'
    ],
    author='G Roques',
    url='https://github.com/gbroques/ose-workbench-core',
    description='Core library common to all OSE workbenches.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
    include_package_data=True,
    classifiers=[
        # Full List: https://pypi.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
