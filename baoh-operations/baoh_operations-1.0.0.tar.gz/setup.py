from setuptools import setup

setup(name="baoh_operations",
      version="1.0.0",
      description="My pypi package for basic algebra",
      packages=['baoh_operations'],
      author="Bao Hoang",
      author_email="baohoang.1988@gmail.com",
      zip_safe=False)


#cd binomial_package_files
#python setup.py sdist
#pip install twine

# commands to upload to the pypi test repository
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#pip install --index-url https://test.pypi.org/simple/ dsnd-probability

# command to upload to the pypi repository
#twine upload dist/*
#pip install dsnd-probability
#