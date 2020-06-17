import os
import sys
import re
from aos.util import get_host_os, get_aos_version, locale_to_unicode
from aos.managers.constant import *
from aos.managers.misc import version_greater_than, version_not_less_than, aos_warning
from aos.constant import NO_AOSSRC_HINT

def check_aos_src_root(dir):
    original_dir = os.getcwd()
    host_os = get_host_os()
    if host_os == 'Win32':
        sys_root = re.compile(r'^[A-Z]{1}:\\$')
    else:
        sys_root = re.compile('^/$')

    os.chdir(dir)

    while os.path.isdir('/'.join(['.', aos_src_dir_chk1])) == False or \
          os.path.isdir('/'.join(['.', aos_src_dir_chk2])) == False:
        os.chdir('../')
        if sys_root.match(os.getcwd()):
            if os.path.isdir(original_dir):
                os.chdir(original_dir)
            return 'fail', None

    aos_root_dir = os.getcwd()

    if os.path.isdir(original_dir):
        os.chdir(original_dir)

    return 'success', aos_root_dir

class LocalPkg():
    def __init__(self):
        self.aos_src_root = None
        pass

    def __enter__(self):
        return self

    def __exit(self, exc_type, exc_value, traceback):
        pass

    def validate(self):
        # Check if curdir is a valid aos root first
        curdir = os.getcwd()
        ret, dir = check_aos_src_root(curdir)

        if ret == 'success':
            self.aos_src_root = os.path.abspath(dir)
        else:
            """
            # If curdir not hit, then check if AOS_SDK_PATH environment
            # variable indicates a valid aos root
            """
            aos_sdk_path = os.environ.get("AOS_SDK_PATH")
            if aos_sdk_path and os.path.isdir(aos_sdk_path):
                ret, dir = check_aos_src_root(aos_sdk_path)
                if ret == 'success':
                    self.aos_src_root = os.path.abspath(dir)

        if not self.aos_src_root:
            aos_warning(NO_AOSSRC_HINT)
            return False
        else:
            # aos_src_root will be widely used, so unicode encoding.
            # otherwise errors in ' aos_src_root + str' and str.join() cases.
            self.aos_src_root = locale_to_unicode(self.aos_src_root)

            osver = self.getOsVersion()
            if not osver:
                aos_warning("Failed to find AliOS Things version inforamtion!")
                return False

            if not version_not_less_than(osver, ADDON_OS_VER_BASE):
                aos_warning("\nThis command is not supported on your verson "
                          "of AliOS Things!\nYour version is '%s' while minimal "
                          "supported version is '%s'." % (osver, ADDON_OS_VER_BASE))
                return False

        return True

    # Return a dictionary with specified pakcage name with version information
    def getPackagesWithVersion(self, searchall, names=[]):
        pkgs_info = []

        pkgdirs = list(OS_COMPONENT_DIRS)

        if searchall:
            pkgdirs.extend(list(OS_PLATFORM_DIRS))

        pkgdirs = set(pkgdirs)

        for dir in pkgdirs:
            dir_to_walk = os.path.abspath(self.aos_src_root + os.path.sep + dir)
            for dirpath, dirnames, filenames in os.walk(dir_to_walk, topdown=True):
                if not "aos.mk" in filenames:
                    continue
                else:
                    pkgname = None
                    pkgver = None
                    filename = os.path.abspath(dirpath + os.path.sep + 'aos.mk')
                    with open(filename, "r") as f:
                        data = f.read().splitlines()
                        for line in data:
                            #if "NAME :=" in line or "NAME:=" in line:
                            if not pkgname and re.findall(r'^.*NAME\s*:?=.+', line):
                                pkgname = re.findall(r'.*=\s*(\S+)', line)
                                # Skip if not in the specified name list
                                if names and pkgname and not pkgname[0] in names:
                                    break
                                else:
                                    continue
                            if not pkgver and re.findall(r'^.*\$\(NAME\)_VERSION\s*:?=.+', line):
                                pkgver = re.findall(r'.*=\s*(\S+)', line)
                                break

                    if names and pkgname and not pkgname[0] in names:
                        continue

                    # hack for yts and umesh lib comp
                    #if pkgname[0] in ['yts', 'umesh', 'umesh2'] and 'publish' in dirpath.split(os.path.sep):
                    #    continue

                    # append to dict
                    if pkgname and pkgver:
                        keys = [pkg_name_in_dict, pkg_version_in_dict, pkg_localdir_in_dict]
                        values = [pkgname[0], pkgver[0], dirpath]
                        tmp = dict(zip(keys, values))
                        pkgs_info.append(tmp)

        # Sort by name
        k = lambda s:s[pkg_name_in_dict]
        pkgs_info.sort(key=k)

        return pkgs_info

    # Get local OS version
    def getOsVersion(self):
        # TODO
        # get the os version from include/aos/kernel.h:SYSINFO_KERNEL_VERSION?
        return get_aos_version(root=self.aos_src_root)

    def getDependency(self, name):
        dep = []

        pkgdirs = list(OS_COMPONENT_DIRS)

        if not isinstance(name, str) or not name:
            warning("No pkg name provided!")
            return dep

        if name.startswith("mcu_") or \
           name.startswith("board_") or \
           name.startswith("arch_"):
            pkgdirs.extend(list(OS_PLATFORM_DIRS))

        pkgdirs = set(pkgdirs)

        pkg_found = False
        for dir in pkgdirs:
            dir_to_walk = os.path.abspath(self.aos_src_root + os.path.sep + dir)
            for dirpath, dirnames, filenames in os.walk(dir_to_walk, topdown=True):
                if not "aos.mk" in filenames:
                    continue
                else:
                    mkfile = os.path.abspath(dirpath + os.path.sep + 'aos.mk')
                    with open(mkfile, "r") as f:
                        data = f.read().splitlines()
                        for line in data:
                            if re.findall(r'^.*NAME\s*:?=.+', line):
                                pkgname = re.findall(r'.*=\s*(\S+)', line)
                                if pkgname and name == pkgname[0]:
                                    pkg_found = True
                                break

                        if pkg_found:
                            break

            if pkg_found:
                break

        if pkg_found:
            with open(mkfile, "r") as f:
                #data = f.read().splitlines()
                l = f.readline()
                while l:
                    comps = re.findall(r'^\s*\$\(NAME\)_COMPONENTS.*=\s*(\S+)', l)
                    if comps:
                        comps = re.split(r'[\s]', comps[0])
                        if comps:
                            dep.extend(comps)

                        while re.findall(r'.*\\\s*$', l):
                            l = f.readline()
                            comps = re.split(r'[\s]', l)
                            if comps:
                                dep.extend(comps) 

                    l = f.readline()

        return dep

    '''names provided in a list of str.'''
    def getMissingPackages(self, names):
        missing = []

        local_found = self.getPackagesWithVersion(True, names)
        local_found = map(lambda x:x[pkg_name_in_dict], local_found)
        missing = set(names) - set(local_found)

        return missing

    '''namevers provided in a list of dict:
       {"min":'x.x.x[.x]', "max":'x.x.x[.x]', "name":'xxx'}
    '''
    def getMissingVersionedPackages(self, namevers):
        missing = []

        if not namevers:
            return []

        local_found = self.getPackagesWithVersion(True, \
                      list((lambda x:x[DEP_NAME])(x) for x in namevers))

        for p in namevers:
            matched = False
            name = p[DEP_NAME]
            minver = p[DEP_VER_MIN]
            maxver = p[DEP_VER_MAX]
            for lp in local_found:
                if name == lp[pkg_name_in_dict]:
                    ver = lp[pkg_version_in_dict]
                    if not version_greater_than(ver, maxver) and not version_greater_than(minver, ver):
                        matched = True
                        break
            if not matched:
                missing += [name]

        return missing
