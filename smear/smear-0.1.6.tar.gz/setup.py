import os
import inspect
from setuptools import setup
from smear.version import version as version

# The directory containing this file
this_script_dir = os.path.dirname(inspect.stack()[0][1])

# The text of the README file
with open(os.path.join(this_script_dir, "pip_readme.md"), 'r') as readme_file:
    readme = readme_file.read()

# This call to setup() does all the work
setup(
    name="smear",
    version=version,
    description="Clear CLI interface for smearing",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/eic/escalate/smear",
    author="Dmitry Romanov",
    author_email="romanov@jlab.org",
    license="MIT",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["smear"],
    include_package_data=True,
    setup_requires=["pyjano"],
    install_requires=["pyjano"],
    entry_points={
        "console_scripts": [
            "smear=smear:smear_cli",
        ]
    },
)