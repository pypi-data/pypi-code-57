import setuptools

setuptools.setup(
    name="koreanWikiExtractor_test2",
    version="0.1",
    license='MIT',
    author="Kim Jaehun",
    author_email="wogjs217@gmail.com",
    description="convert MediaWiki to plain text",
    long_description=open('README.md').read(),
    url="https://github.com/Kim-Jaehun/Korean-WikiExtractor",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3.6",
    ],
)
