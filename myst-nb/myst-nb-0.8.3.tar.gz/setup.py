"""MyST-NB package setup."""
from setuptools import find_packages, setup

# Manually finding the version so we don't need to import our module
text = open("./myst_nb/__init__.py").read()
for line in text.split("\n"):
    if "__version__" in line:
        break
version = line.split("= ")[-1].strip('"')

setup(
    name="myst-nb",
    version=version,
    description=(
        "A Jupyter Notebook Sphinx reader built on top of the MyST markdown parser."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/executablebooks/myst_nb",
    author="ExecutableBookProject",
    author_email="choldgraf@berkeley.edu",
    license="BSD-3",
    packages=find_packages(),
    entry_points={"console_scripts": []},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Framework :: Sphinx :: Extension",
    ],
    keywords="markdown lexer parser development docutils sphinx",
    python_requires=">=3.6",
    package_data={"myst_nb": ["_static/*"]},
    install_requires=[
        "myst-parser~=0.8",
        "docutils>=0.15",
        "sphinx>=2,<3",
        "jupyter_sphinx>=0.2.4",
        "ipython",
        "nbformat",
        "nbconvert",
        "nbclient",
        "jupyter-cache~=0.2.1",
        "pyyaml",
        "sphinx-togglebutton",
    ],
    extras_require={
        "code_style": ["flake8<3.8.0,>=3.7.0", "black", "pre-commit==1.17.0"],
        "testing": [
            "pytest~=5.4",
            "pytest-cov~=2.8",
            "coverage<5.0",
            "pytest-regressions",
            "matplotlib",
            "numpy",
            "sympy",
            "pandas",
        ],
        "rtd": [
            "sphinxcontrib-bibtex",
            "ipywidgets",
            "pandas",
            "numpy",
            "sympy",
            "altair",
            "alabaster",
            "bokeh",
            "plotly",
            "matplotlib",
            "sphinx-copybutton",
            "sphinx-book-theme",
        ],
    },
    zip_safe=True,
)
