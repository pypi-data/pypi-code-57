# coding: utf-8

# @Time:2020/3/15 12:34
# @Auther:sahala


from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="super_sweetest",  # 这里是pip项目发布的名称
    version="1.1.9",  # 版本号，数值大的会优先被pip
    keywords=("pip", "super_sweetest", "featureextraction"),
    description="automation tools",
    long_description="automation tools: requests,appium,selenium,air_android,air_ios,adb,poco......相对坐标点击",
    license="MIT Licence",

    url="https://github.com/",  # 项目相关文件地址，一般是github
    author="liyubin",
    author_email="1399393088@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
                      "Appium-Python-Client",
                      "certifi",
                      "chardet",
                      "idna",
                      "injson",
                      "Pillow",
                      "requests",
                      "selenium",
                      "urllib3",
                      "xlrd",
                      "XlsxWriter",
                      "airtest",
                      "pocoui",
					  "validator_sa",
                      ]  # 这个项目需要的第三方库
)



# 步骤：

# 1.setup.py放在被打包同级
    # 本地打包项目文件
    # python setup.py sdist

# 2.上传项目到pypi服务器
    # pip install twine
    # twine upload dist/name.tar.gz

# 3.下载上传的库
    # pip install name
