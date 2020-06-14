import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-securefields',
    version='0.0.1',
    packages=['securefields'],
    description='A Django module for managing secure database model fields.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='5 Health Inc',
    author_email='hello@botmd.io',
    url='https://github.com/fivehealth/django-securefields',
    license='MIT License',
    install_requires=[
        'django>=2.2',
        'cryptography>=2.9',
    ],
    python_requires='>=3',
    keywords='django security encryption hashing hmac aes',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'License :: OSI Approved :: MIT License',
    ],
)
