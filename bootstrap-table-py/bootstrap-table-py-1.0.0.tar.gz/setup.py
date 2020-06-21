from setuptools import setup, find_packages

setup(
    name="bootstrap-table-py",
    author="The Pycroft Authors",
    description="Python wrapper for bootstrap-table",
    long_description=__doc__,
    version="1.0.0",
    url="https://github.com/agdsn/bootstrap-table-py/",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">= 3.5",
    license="Apache Software License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
