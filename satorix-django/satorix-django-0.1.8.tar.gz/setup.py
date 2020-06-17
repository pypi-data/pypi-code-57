from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="satorix-django",
    version="0.1.8",
    description="Configure Django application for Satorix environment",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/satorix/satorix-django",
    author="Satorix",
    author_email="tech@satorix.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    packages=["satorix_django"],
    include_package_data=True,
    install_requires=[
        "django>=2.2.11",
        "django-heroku",
    ],
    test_suite='nose2.collector.collector',
    tests_require=[
        'nose2',
        'testfixtures',
    ],
    entry_points={
        "console_scripts": [
            "satorix-django-config=satorix_django.__main__:main",
        ]
    },
)
