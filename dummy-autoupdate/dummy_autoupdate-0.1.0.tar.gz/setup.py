from setuptools import setup, find_packages

from dummy_autoupdate import __version__

setup(
    name='dummy_autoupdate',
    packages=find_packages(),
    version=__version__,
    author='Vladimir Starostin',
    author_email='vladimir.starostin@uni-tuebingen.de',
    description='Dummy autoupdate for testing',

    license='MIT',
    python_requires='>=3.7.2',
    entry_points={
            "gui_scripts": [
                "dummy_autoupdate = dummy_autoupdate:run",
            ]
        },
    install_requires=[
        'PyQt5',
        'requests'
        ]
)
