import sys
import os.path
from setuptools import setup
import pgzero



install_requires = [
    'pygame>=1.9.2, <2.0',
    'numpy',
]

extras_require = {
    ':python_version < "3.4"': ["enum34"],
}

setup(
    name='mc_pgzrun',
    version="0.7",
    description="自用自改零模板二维游戏框架",
    author='Hugn',
    author_email='wang1183478375@outlook.com',
    url='http://pypi.python.org/pypi/mc_pgzrun',
    packages=['pgzero'],
    data_files=[('pgzero/data',['pgzero/data/icon.png',
                                'pgzero/data/joypad.png'])],
    include_package_data=True,
    py_modules=['mc_pgzrun'],
    entry_points={
        'console_scripts': [
            'mc_pgzrun = pgzero.runner:main'
        ]
    },
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Education',
        'Topic :: Games/Entertainment',
    ],
    test_suite='test',
    zip_safe=False
)
