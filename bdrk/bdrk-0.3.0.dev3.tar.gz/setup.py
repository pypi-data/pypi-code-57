import setuptools
from setuptools import find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.md", "r") as changelog_file:
    changelog = changelog_file.read()

# We keep VERSION in a file so that it is much easier to access programmatically
# Please remember to bump the version in the VERSION file
with open("VERSION", "r") as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name="bdrk",
    version=version,
    author="basis-ai.com",
    author_email="contact@basis-ai.com",
    description="Client library for Bedrock platform",
    long_description=readme + "\n\n" + changelog,
    long_description_content_type="text/markdown",
    url="https://github.com/basisai/span",
    install_requires=[
        "requests>=2.2,<3.0",
        "six>=1.14.0,<2.0",
        "numpy>=1.11,<2",
        "pandas>=1.0,<2.0",
        "aif360>=0.2.3,<1.0",
        "shap>=0.35.0,<1.0",
    ],
    extras_require={
        "cli": ["Click", "docker", "jsonschema", "pyhcl"],
        "model-monitoring": ["fluent-logger", "prometheus_client", "numpy"],
    },
    packages=find_packages(),
    package_data={"": ["*.hcl", "README.md", "CHANGELOG.md"]},
    exclude_package_data={"": ["README.md", "CHANGELOG.md", "notebooks/**/*"]},
    classifiers=["Programming Language :: Python :: 3"],
    entry_points={"console_scripts": ["bdrk = bedrock_client.bedrock.main:main [cli]"]},
)
