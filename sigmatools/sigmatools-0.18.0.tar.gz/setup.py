# Setup module for Sigma toolchain
# derived from example at https://github.com/pypa/sampleproject/blob/master/setup.py
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sigmatools',
    version='0.18.0',
    description='Tools for the Generic Signature Format for SIEM Systems',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Neo23x0/sigma',
    author='Sigma Project',
    author_email='thomas@patzke.org',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: Security',
        'Topic :: Internet :: Log Analysis',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
    ],
    keywords='security monitoring siem logging signatures elasticsearch splunk ids sysmon',
    packages=[
        'sigma',
        'sigma.backends',
        'sigma.config',
        'sigma.parser',
        'sigma.parser.modifiers',
        ],
    python_requires='~=3.6',
    install_requires=['PyYAML', 'pymisp', 'progressbar2'],
    extras_require={
        'test': ['coverage', 'yamllint'],
    },
    data_files=[
        ('etc/sigma', [
            "config/arcsight.yml",
            "config/carbon-black.yml",
            "config/ecs-proxy.yml",
            "config/filebeat-defaultindex.yml",
            "config/helk.yml",
            "config/limacharlie.yml",
            "config/logpoint-windows.yml",
            "config/logstash-defaultindex.yml",
            "config/logstash-linux.yml",
            "config/logstash-windows.yml",
            "config/mitre/tactics.json",
            "config/mitre/techniques.json",
            "config/netwitness.yml",
            "config/powershell.yml",
            "config/qradar.yml",
            "config/qualys.yml",
            "config/splunk-windows-index.yml",
            "config/splunk-windows.yml",
            "config/splunk-zeek.yml",
            "config/sumologic.yml",
            "config/thor.yml",
            "config/winlogbeat-modules-enabled.yml",
            "config/winlogbeat-old.yml",
            "config/winlogbeat.yml",
            ]),
        ('etc/sigma/generic', [
            'config/generic/sysmon.yml',
            'config/generic/windows-audit.yml',
        ])],
    entry_points={
        'console_scripts': [
            'sigmac = sigma.sigmac:main',
            'merge_sigma = sigma.merge_sigma:main',
            'sigma2misp = sigma.sigma2misp:main',
            'sigma2attack = sigma.sigma2attack:main',
            'sigma_similarity = sigma.sigma_similarity:main',
            'sigma_uuid = sigma.sigma_uuid:main',
        ],
    },
)
