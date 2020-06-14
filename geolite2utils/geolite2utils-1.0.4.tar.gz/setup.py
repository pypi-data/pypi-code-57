from setuptools import setup, find_packages


with open('VERSION.txt') as f:
    version = f.readline()


setup(
    name='geolite2utils',
    version=version,
    url='https://github.com/matix-io/python-geolite2utils',
    license='MIT',
    description='Download, extract, and use MaxMind GeoLite2 databases from Python.',
    long_description='',
    author='Connor Bode',
    author_email='connor@matix.io',
    packages=find_packages(),
    install_requires=[
		'requests',
		'geoip2',
	],
    zip_safe=False,
    classifiers=[],
)
