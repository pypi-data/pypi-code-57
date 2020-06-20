import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()


setup(
    name='django-extensions-models',
    version='0.1',
    packages=find_packages(),
    description='model extensions with timestamp and uuid and more',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Thomas Adel',
    author_email='thomas.adel31@gmail.com',
    url='https://github.com/thomas545/django-extensions-models',
    keywords='django-models-extensions model-extensions django-extensions',
    zip_safe=False,
    license='MIT',
    install_requires=[
        'Django>=2.0',
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        'Framework :: Django',
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
    python_requires='>=3.5',
)