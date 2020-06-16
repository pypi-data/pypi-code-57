from setuptools import setup

setup(
    name='ose-workbench-core',
    version='0.1.0a1',
    packages=[
        'osecore',
        'osecore.app',
        'osecore.app.attachment',
        'osecore.app.cut_list',
        'osecore.app.shape',
        'osecore.gui',
        'osecore.gui.cut_list',
        'osecore.gui.selection'
    ],
    author='G Roques',
    url='https://github.com/gbroques/ose-workbench-core',
    description='Core library common to all OSE workbenches.',
    install_requires=[],
    include_package_data=True,
    classifiers=[
        # Full List: https://pypi.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
