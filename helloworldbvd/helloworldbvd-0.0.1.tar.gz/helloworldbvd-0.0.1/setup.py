from setuptools import setup

setup(
    name='helloworldbvd',
    url="https://gitlab.com/bvd-sketchbook/package-pypi",
    author="Bastiaan Van denabeele",
    author_email="vandenabeele.bastiaan@gmail.com",
    version='0.0.1',
    description='Say Hello!',
    py_modules=["helloworldbvd"],
    package_dir={'':'src'},
    install_requires = [],
    extras_require = {
        "dev": [
            "pytest>=5.4.3",
            "twine>=3.2.0"
        ]
    },
)