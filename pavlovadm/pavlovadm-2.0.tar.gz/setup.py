#!/usr/bin/env python

from distutils.core import setup
import setuptools


from pavlovadm import __pkginfo__

pkginfo = {}
for i in dir(__pkginfo__):
	if i.startswith('__'): continue
	pkginfo[i] = getattr(__pkginfo__, i)
pkginfo['packages'] = setuptools.find_packages()
print('\n'.join('%s = %s'%(k, v) for (k, v) in pkginfo.items()))
setup(**pkginfo)
