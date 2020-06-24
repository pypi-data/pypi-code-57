from pathlib import Path
from setuptools import setup

with open(Path(__file__).parent.joinpath("VERSION")) as f:
    version = f.readline()

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="quantbacktest",
    version=version,
    description="This backtesting is used to backtest algorithmic/quant trading strategies.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Jan Frederic Spörer",
    author_email="jan.spoerer@whu.edu",
    license="BSD two-clause license",
    packages=["quantbacktest"],
    # install_requires=["datetime", "numpy", "matplotlib", "pandas"],
    url="https://gitlab.com/fsbc/theses/quantbacktest",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "FullBacktest=quantbacktest.__main__:main",
        ]
    },
    include_package_data=True,
) # Sources of this setup.py: Jonathan Hsu (Medium article) and Geir Arne Hjelle (Realpython)
# https://medium.com/better-programming/how-to-publish-your-first-python-package-its-not-that-hard-6202f74f5954
# https://realpython.com/pypi-publish-python-package/
# https://www.youtube.com/watch?v=wCGsLqHOT2I
