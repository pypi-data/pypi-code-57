from distutils.core import setup
setup(
    name='Keen_SuperMath', # 对外我们模块的名字
    version='1.0.0', # 版本号
    description='这是第一个对外发布的模块，测试哦', # 描述
    author='Keen', # 作者
    author_email='keenl@me.com', py_modules=['Keen_SuperMath.demo1','Keen_SuperMath.demo2'] # 要发布的模块
)