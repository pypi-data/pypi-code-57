from distutils.core import setup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

setup(
    name=        'wll',
    version='1.1.0',
    py_modulse   =['wll'],
    author= 'taish',
    author_email='2136980981@qq.com',
    url='https://upload.pypi.org/legacy/',description=' A printer of log list',
)