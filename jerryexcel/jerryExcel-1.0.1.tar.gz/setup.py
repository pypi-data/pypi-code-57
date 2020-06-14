import setuptools

with open(file="README.md", mode="r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jerryExcel",
    version="1.0.1",
    author="JerryLaw",
    author_email="623487850@qq.com",
    description="A tool for excel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JeansLaw/excelUtil.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'xlrd',
        'xlutils',
        'xlwt'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)