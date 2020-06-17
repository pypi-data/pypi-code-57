from setuptools import setup, find_packages

setup(
    name='yamlito',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/hzanoli/yamlito',
    license='GNU Lesser General Public License v3.0',
    author='Henrique Zanoli',
    author_email='hzanoli@gmail.com',
    description='Simple yaml config loader',
    install_requires=['PyYAML'],
    test_requires=['pytest', 'pytest-cov', 'coverage'],
    test_suite='pytest'
)
