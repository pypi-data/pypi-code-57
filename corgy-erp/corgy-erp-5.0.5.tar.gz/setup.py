import os
from setuptools import setup, find_packages
from distutils.util import convert_path

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

def parse_requirements(filename):
    with open(filename) as f:
        return [line for line in f.read().splitlines() if not line.startswith('#')]

# ========================================
# Parse requirements for all configuration
# ========================================
install_reqs = parse_requirements(filename=os.path.join('.', 'requirements.txt'))
reqs = [str(ir) for ir in install_reqs]

# ========================================
# Readme
# ========================================
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

PROJECT_NAME = 'corgy_erp'

# ========================================
# Version parsing
# ========================================
main_ns = {}
ver_path = convert_path(PROJECT_NAME + '/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


# data_files = []
# for dirpath, dirnames, filenames in os.walk(PROJECT_NAME):
#     for i, dirname in enumerate(dirnames):
#         if dirname.startswith('.'):
#             del dirnames[i]
#     if '__init__.py' in filenames:
#         continue
#     elif filenames:
#         for f in filenames:
#             data_files.append(os.path.join(
#                 dirpath[len(PROJECT_NAME) + 1:], f))



setup(
    name='corgy-erp',
    version=main_ns['__version__'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    description='An opensourse ERP developed on django framework',
    long_description=README,
    long_description_content_type='text/x-rst',
    license='Apache 2.0 License',
    url='https://gitlab.com/corgy/corgy-erp.git',
    author='lordoftheflies',
    author_email='laszlo.hegedus@cherubits.hu',
    classifiers=[
        'Environment :: Web Environment',
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Database'
    ],
    install_requires=reqs,
    scripts=['manage.py'],
)
