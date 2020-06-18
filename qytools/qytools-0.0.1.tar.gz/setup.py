import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
  name="qytools",
  version="0.0.1",
  author="Yulin Qiu",
  author_email="x492876854@qq.com",
  description="QLite3 database reading interface,general SQLite3 database warehousing interface,"
              "general SQLite3 database query assistant tool,stack",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/",
  packages=setuptools.find_packages(),
  classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
