from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='gauss_binomial_mp99',
      version='0.1.3',
      description='Gaussian and Binomial distributions',
	  long_description=long_description,
	  long_description_content_type="text/markdown",
      packages=['gauss_binomial_mp99'],
	  author = 'Manan Paneri',
	  author_email = 'mananpaneri28@gmail.com',
	  url="https://github.com/manan-paneri-99/gauss-binomial-mp99",
      zip_safe=False)
