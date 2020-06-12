from setuptools import setup

setup(
    name='django-configurations-google-analytics',
    version='2020.6.11',
    install_requires=[
        'django-configurations',
        'setuptools',
    ],
    packages=[
        'django_configurations_google_analytics',
        'django_configurations_google_analytics.templatetags',
    ],
)
