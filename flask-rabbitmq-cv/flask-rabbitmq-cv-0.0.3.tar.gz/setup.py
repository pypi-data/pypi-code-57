from setuptools import setup, find_packages

setup(
    name='flask-rabbitmq-cv',
    version='0.0.3',
    author='Pushy',
    author_email='claudiu.vintila@gmail.com',
    url='https://github.com/claudiuvintila/flask-rabbitmq',
    description=u'Let rabbitmq use flask development more easy! ! !',
    packages=find_packages(),
    install_requires=['pika']
)