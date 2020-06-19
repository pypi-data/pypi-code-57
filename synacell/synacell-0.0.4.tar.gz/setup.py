import setuptools
from setuptools import Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="synacell",
    version="0.0.4",
    author="Ginko Balboa",
    author_email="ginkobalboa3@gmail.com",
    description="Synapses and cells",
    packages=['synacell',
              'synacell.cmodule',
              'synacell.test'],
    package_dir={'synacell': 'synacell',
                 'synacell.cmodule': 'synacell/cmodule',
                 'synacell.test': 'synacell/test'},
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GinkoBalboa/synacell",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: C++",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    python_requires='>=3.7',
    zip_safe=False,
)
