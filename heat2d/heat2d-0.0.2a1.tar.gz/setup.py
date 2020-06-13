#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name="heat2d",
    packages = find_packages(),
    version="0.0.2a1",
    author="Kadir Aksoy",
    author_email="kursatkadir014@gmail.com",
    description="A simple 2D game engine",
    url="https://github.com/kadir014/heat2d",
    project_urls={
    'Documentation': 'https://kadir014.github.io/projects/heat2d/index.html',
    },
    keywords='game engine development 2d',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["pygame>=1.9.6"]
)
