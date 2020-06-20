from setuptools import setup, find_packages

VERSION = '0.0.2'

setup(name='anndb',
    version=VERSION,
    description='AnnDB Client',
    author='Marek Galovic',
    author_email='galovic.galovic@gmail.com',
    license='MIT',
    url='https://github.com/marekgalovic/anndb-client-python',
    download_url='https://github.com/marekgalovic/anndb-client-python/archive/%s.tar.gz' % VERSION,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'grpcio'
    ],
)