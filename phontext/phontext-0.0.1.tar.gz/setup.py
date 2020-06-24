import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="phontext",
  version="0.0.1",
  author="Rolando Muñoz Aramburú",
  author_email="rolando.muar@gmail.com",
  description="Phonology analysis",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/rolandomunoz/phontext",
  packages=setuptools.find_packages(),
  classifiers=[
      "Topic :: Text Processing :: Linguistic"
  ],
  python_requires='>=3.6',
)
