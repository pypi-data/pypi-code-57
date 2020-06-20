from setuptools import setup, find_packages

print('PACKAGES: ',find_packages())

# Parse the version from the module.
with open('busylite/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

# get readme
with open('README.md') as f:
    readme = f.read()

setup(name='busylite',
      version=version,
      description='Package to interact with a Kuando Busylight',
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://gitlab.com/ryanmcginger/busylite",
      classifiers=[
        'Programming Language :: Python :: 3.8',
      ],
      keywords='busylight hid busylite',
      author='Ryan McCarthy',
      author_email='code@mcginger.net',
      license='MIT License',
      install_requires=[
        'click',
        'numpy',
        'hidapi',
        'flask',
        'flask-httpauth',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      package_dir={'': '.'},
      packages=find_packages(),
      entry_points='''
        [console_scripts]
        busycli=busylite.scripts.busycli:cli
      ''',
      include_package_data=True,
      zip_safe=False)
