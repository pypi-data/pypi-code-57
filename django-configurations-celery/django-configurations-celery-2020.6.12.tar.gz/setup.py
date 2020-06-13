from setuptools import setup

setup(
    name='django-configurations-celery',
    version='2020.6.12',
    install_requires=[
        'celery',
        'django-configurations',
        'setuptools',
    ],
    packages=[
        'django_configurations_celery',
    ],
)
