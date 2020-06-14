from setuptools import setup, find_packages


with open('VERSION.txt') as f:
    version = f.readline()


setup(
    name='django-fixed-timezone-field',
    version=version,
    url='https://github.com/matix-io/django-fixed-timezone-field',
    license='MIT',
    description='Ignore the activated timezone.',
    long_description='',
    author='Connor Bode',
    author_email='connor@matix.io',
    packages=find_packages(),
    install_requires=[],
    zip_safe=False,
    classifiers=[],
)
