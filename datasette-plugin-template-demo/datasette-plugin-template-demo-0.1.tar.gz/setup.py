from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-plugin-template-demo",
    description="Demonstrating https://github.com/simonw/datasette-plugin",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-plugin-template-demo",
    project_urls={
        "Issues": "https://gitlab.com/simonw/datasette-plugin-template-demo/issues",
        "CI": "https://github.com/simonw/datasette-plugin-template-demo/actions",
        "Changelog": "https://github.com/simonw/datasette-plugin-template-demo/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_plugin_template_demo"],
    entry_points={"datasette": ["plugin_template_demo = datasette_plugin_template_demo"]},
    install_requires=["datasette"],
    extras_require={
        "test": ["pytest", "pytest-asyncio", "httpx"]
    },
    tests_require=["datasette-plugin-template-demo[test]"],
)
