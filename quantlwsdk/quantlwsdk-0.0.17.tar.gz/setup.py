from setuptools import setup
import setuptools



pcg=[]
pcg.extend(setuptools.find_packages('pyalgotrade'))
pcg.extend(setuptools.find_packages('highcharts'))

ss1=setuptools.find_packages(exclude=["backtrader.*", "rqalpha.*", "rqalpha-back.*"])
ss=setuptools.find_packages('pyalgotrade\\')

setup(
    name='quantlwsdk',
    version='0.0.17',
    author='lw',
    author_email='100000@qq.com',
    url='https://github.com',
    description=u'量化辅助sdk',
    packages=ss1,
include_package_data=True
)

#
# setup(
#     name='quantlwsdk',
#     version='0.0.4',
#     author='lw',
#     author_email='100000@qq.com',
#     url='https://github.com',
#     description=u'量化辅助sdk',
#     # packages=setuptools.find_packages(),
#     packages=['highcharts','pyalgotrade'],
#     install_requires=[],
#     include_package_data=True    # 启用清单文件MANIFEST.in
# )