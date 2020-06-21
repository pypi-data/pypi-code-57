import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="wxgbot",
    version="1.3",
    author="wanghaiyang",
    author_email="why13082847531@163.com",
    description="企业微信机器人发送消息",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/LZC6244/maida",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
