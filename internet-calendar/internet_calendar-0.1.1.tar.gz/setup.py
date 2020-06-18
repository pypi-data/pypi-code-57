from setuptools import setup

setup(
    name='internet_calendar',
    version='0.1.1',
    packages=['internet_calendar'],
    url='',
    install_requires=["requests", "bs4", "pendulum", "requests-cache"],
    license='MIT',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='unofficial api for https://forekast.com/'
)
