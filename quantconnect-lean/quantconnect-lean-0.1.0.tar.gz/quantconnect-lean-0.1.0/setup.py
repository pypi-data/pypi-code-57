import pathlib
from setuptools import setup

setup(
    name='quantconnect-lean',
    version='0.1.0',
    description='QuantConnect package reserved for future use',
    author='QuantConnect Corp.',
    author_email='support@quantconnect.com',
    license='Apache 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License'
    ],
    packages=[
        'QuantConnect_Reserved',
    ],
    package_data={
        'QuantConnect': ['py.typed', '*.pyi'],
        'QuantConnect.Data': ['py.typed', '*.pyi'],
        'QuantConnect.Securities': ['py.typed', '*.pyi'],
        'QuantConnect.Algorithm': ['py.typed', '*.pyi'],
    },
    python_requires='>=3.6'
)
