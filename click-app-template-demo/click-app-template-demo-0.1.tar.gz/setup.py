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
    name="click-app-template-demo",
    description="Demonstrating https://github.com/simonw/click-app",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/click-app-template-demo",
    project_urls={
        "Issues": "https://github.com/simonw/click-app-template-demo/issues",
        "CI": "https://github.com/simonw/click-app-template-demo/actions",
        "Changelog": "https://github.com/simonw/click-app-template-demo/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["click_app_template_demo"],
    entry_points="""
        [console_scripts]
        click-app-template-demo=click_app_template_demo.cli:cli
    """,
    install_requires=["click"],
    extras_require={
        "test": ["pytest"]
    },
    tests_require=["click-app-template-demo[test]"],
)
