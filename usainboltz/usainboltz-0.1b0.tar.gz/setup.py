# coding: utf8

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

with open("README.md", "r") as file:
    long_description = file.read()

extensions = [
    Extension(
        "usainboltz.generator",
        sources=["src/usainboltz/generator.pyx", "src/xoshiro/xoshiro.c"],
        include_dirs=["src/xoshiro"],
        extra_compile_args=["-std=c99"]
    )
]

cython_aliases = None
include_dirs = None
exclude_packages = ["xoshiro"]

try:
    from sage import env

    cython_aliases = env.cython_aliases()
    include_dirs = env.sage_include_directories()
except ImportError:
    pass

setup(
    name="usainboltz",
    version="0.1b0",
    author="Matthieu Dien, Martin Pépin",
    author_email="kerl@wkerl.me",
    description="Fast Boltzmann random generators for SageMath",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ParComb/usain-boltz",
    project_urls={
        "Bug Tracker": "https://gitlab.com/ParComb/usain-boltz/issues",
        "Documentation": "https://usain-boltz.readthedocs.io",
        "Source Code": "https://gitlab.com/ParComb/usain-boltz",
    },
    packages=find_packages("src", exclude=exclude_packages),
    package_dir={"": "src"},
    ext_modules=cythonize(extensions, aliases=cython_aliases, language_level=3),
    install_requires=["paganini >= 1.3.2"],
    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "Programming Language :: C",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    include_dirs=include_dirs,
    python_requires=">=3.6",
)
