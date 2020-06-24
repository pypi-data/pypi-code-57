import os
from setuptools import setup, find_packages

if os.environ.get('READTHEDOCS') == 'True':
    install_requires = [
        'typing_extensions>=3.7.4',
    ]
else:
    install_requires = [
        'jinja2>=2.10.1',
        'numpy>=1.17.2',
        'pandas>=0.25.1',
        'pint>=0.9',
        'scipy>=1.2.1',
        'torch>=1.2.0',
        'typing_extensions>=3.7.4',
    ]

with open('README.rst') as fh:
    readme = fh.read()

setup(
    name='DiPAS',
    use_scm_version=True,
    description='DiPAS is a framework for differentiable simulations of particle accelerators.',
    long_description=readme,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords=['simulation', 'framework', 'particle tracking', 'accelerator', 'optimization', 'differentiable'],
    url='https://gitlab.com/Dominik1123/dipas',
    author='Dominik Vilsmeier',
    author_email='d.vilsmeier@gsi.de',
    license='GPL-3.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'madx-to-html = dipas.tools.madx_to_html:main',
        ],
    },
    install_requires=install_requires,
    tests_require=['coverage'],
    python_requires='>=3.7',
    include_package_data=True,
)

