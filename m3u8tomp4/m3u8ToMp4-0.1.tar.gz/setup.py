import setuptools
import subprocess

setuptools.setup(
    name="m3u8ToMp4",
    version="0.1",
    description="download video by m3u8 url",
    url="https://github.com/yfd-01/m3u8ToMp4",
    author="VioletYFD",
    author_email="2448543261@qq.com",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["requests", "pycryptodome"],
    zip_safe=False
)