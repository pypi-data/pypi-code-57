#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shunxing Bao <shunxing.bao@vanderbilt.edu>'

import os
from recon_stats import __version__

from setuptools import setup, find_packages


if __name__ == '__main__':

    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    setup(name='recon-stats_ldax',
        author='Scott Burns',
        author_email='onealbao@gmail.com',
        description='recon-stats-ldax is a simple package to parse stats files from Freesurfer recon-all',
        license='BSD (3-clause)',
        url='http://github.com/VUIIS/recon-stats',
        version=__version__,
        download_url='http://github.com/VUIIS/recon-stats',
        long_description='''The repo is an update fix version for sburns/recon-stats. The original repo seems to be no logner maintained.''',
        packages=find_packages(),
        platforms='any',
        classifiers=(
                #'Development Status :: 1 - Planning',
                'Development Status :: 2 - Pre-Alpha',
                # 'Development Status :: 3 - Alpha',
                #'Development Status :: 4 - Beta',
                #'Development Status :: 5 - Production/Stable',
                #'Development Status :: 6 - Mature',
                #'Development Status :: 7 - Inactive',
                'Intended Audience :: Developers',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: BSD License',
                'Topic :: Software Development',
                'Topic :: Scientific/Engineering',
                'Operating System :: POSIX',
                'Operating System :: Unix',
                'Operating System :: MacOS',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3.6',
                'Topic :: Scientific/Engineering',)
        )
