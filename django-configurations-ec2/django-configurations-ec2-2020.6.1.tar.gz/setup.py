from setuptools import setup

setup(
    name='django-configurations-ec2',
    version='2020.6.1',
    install_requires=[
        'boto3',
        'django-configurations',
        'requests',
        'setuptools',
        'watchtower',
    ],
    packages=[
        'django_configurations_ec2',
    ],
)
