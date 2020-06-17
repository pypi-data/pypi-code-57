import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arris_tg3442_reboot", # Replace with your own username
    version="0.5",
    author="Florian Gabsteiger",
    author_email="florian.g@me.com",
    description="Reboot your Arris TG-3442 router via cli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diveflo/arris-tg3442-reboot",
    packages=setuptools.find_packages(),
    scripts=['arris_tg3442_reboot/reboot.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)