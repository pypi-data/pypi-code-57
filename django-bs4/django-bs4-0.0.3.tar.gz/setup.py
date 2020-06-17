from setuptools import find_packages, setup


setup(
    name='django-bs4',
    description='simple bootstrap4 support for django',
    long_description=open('README.rst').read(),
    version='0.0.3',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
