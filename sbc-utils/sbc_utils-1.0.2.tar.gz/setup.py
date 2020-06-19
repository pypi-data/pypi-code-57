'''
pytz setup script
'''
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

me = 'Abhinav Kotak'
memail = 'in.abhi9@gmail.com'

packages = ['sbc_utils']
package_dir = {'sbc_utils': 'src/sbc_utils'}

setup(
    name='sbc_utils',
    version=os.environ.get('CI_COMMIT_TAG'),
    zip_safe=True,
    description='Utility functions',
    author=me,
    author_email=memail,
    maintainer=me,
    maintainer_email=memail,
    url='https://gitlab.stickboycreative.com/sbc-python/sbc_utils',
    license=open('LICENSE', 'r').read(),
    keywords=['python'],
    packages=packages,
    package_dir=package_dir,
    platforms=['Independant'],
    classifiers=[
        'Development Status :: 1 - beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
