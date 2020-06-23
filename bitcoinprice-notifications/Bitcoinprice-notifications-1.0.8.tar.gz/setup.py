from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()


setup(
    name="Bitcoinprice-notifications",
    version="1.0.8",
    description="A Python package to get Bitcoin price.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Teja-s-au6/Bitocin-Price-Notification",
    author="Teja S",
    author_email="tejaspvg@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Bitcoin_Price_Notifications"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "Bitcoin-Price-Notification=Bitcoin_Price_Notifications.bitcoin_price_notify:main",
        ]
    },
)
