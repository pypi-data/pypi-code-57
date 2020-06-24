from distutils.core import setup
from setuptools import setup

with open("DOC.md", "r") as fh:
    long_description = fh.read()

base_url = 'http://github.com/atmragib/jadukor'
version = '0.0.7'

setup(name='jadukor',
      version=version,
      description='The most powerfull module in the universe',
      long_description=long_description,
      url=base_url,
      download_url='{}/archive/v{}.tar.gz'.format(base_url, version),
      author='A T M Ragib Raihan',
      author_email='atmragibraihan@gmail.com',
      license='MIT',
      packages=['jadukor'],
      keywords=['personal', 'handy', 'ragib', 'jadukor'],
      install_requires=[
          'validators',
          'beautifulsoup4',
      ],
      zip_safe=False,
      classifiers=[
          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          "Operating System :: OS Independent",
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      python_requires='>=3.1',
    #   packages=find_packages(exclude=['tests', 'tests.*']),
    #   package_data={'simple_history': [
    #       'static/js/*.js', 'templates/simple_history/*.html']},
    #   include_package_data=True,
    # use_scm_version=True,
      )
