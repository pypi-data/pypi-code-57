from setuptools import setup, find_packages

print('PACKAGES: ',find_packages())

# Parse the version from the module.
with open('fractalcam/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

# get readme
with open('README.md') as f:
    readme = f.read()

setup(
    name='fractalcam',
    version=version,
    description='Make fractal with USB Webcams',
    long_description=readme,
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    keywords='numpy opencv fractal',
    author='Ryan McCarthy',
    author_email='code@mcginger.net',
    license='MIT',
    install_requires=[
        'numpy',
        # 'numba',
        'scipy',
        'click',
        'opencv-python'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    package_dir={'': '.'},
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        fracam=fractalcam.cli.main:run
    ''',
    zip_safe=False)
