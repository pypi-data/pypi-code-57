import setuptools

# python setup.py sdist
# twine upload --skip-existing --repository pypi dist/*

setuptools.setup(
    name="notify-idle",
    version="0.0.1",
    author="Xiang Chen",
    author_email="xiangchenchen96@gmail.com",
    python_requires=">=3.6",
    scripts=["notify-idle"],
    install_requires=[
        "psutil"
    ],
    description="Send email from GMX if machine is IDLE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
