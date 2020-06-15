import os
from setuptools import setup

requirements = [
    'astunparse>=1.1.0',
]

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'injectify', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/x-rst',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=['injectify'],
    package_dir={'injectify': 'injectify'},
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=requirements,
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Code Generators',
    ],
)
