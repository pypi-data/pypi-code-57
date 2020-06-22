from distutils.core import setup

setup(
    name='hlymode', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦', #描述
    author='hly', # 作者
    author_email='1524489237@qq.com',
    py_modules=['SuperMath.demo1','SuperMath.demo2'] # 要发布的模块
)