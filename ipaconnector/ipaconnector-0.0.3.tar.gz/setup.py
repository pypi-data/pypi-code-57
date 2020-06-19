import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", 'r') as fh:
	requirements = fh.read().split()

setuptools.setup(
    name="ipaconnector",
    version="0.0.3",
    author="Michal Grzejszczak",
    author_email="michal.grzejszczak@ibm.com",
    description="IPA connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    scripts=['scripts/ipa-connector'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
