import pathlib
from setuptools import setup
  
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name="SudokuSolver",
  version="1.0.0",
  description="sudoku solver (9X9)",
  long_description=README,
  long_description_content_type="text/markdown",
  author="Sartak Padhi",
  author_email="sarthakpadhi2016@gmail.com",
  license="AFL-1.1",
  packages=["SudokuSolver"],
  zip_safe=False
)
