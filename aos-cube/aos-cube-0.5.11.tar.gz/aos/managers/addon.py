import os
import sys
import json
import shutil
import re
import zipfile
try:
    from aos.util import aos_input, cd_aos_root, get_host_os, debug
    from aos.managers.misc import aos_info, aos_warning, aos_error, aos_print
    from aos.managers import misc
    from aos.managers import repo
    from aos.managers import sqlitedb
    from aos.constant import OS_REPO, OS_CACHE
    from aos.managers import localpkg
    from aos.managers import rpmfile
    from aos.managers import queryserver
    from aos.managers.constant import *
except Exception as e:
    print("Exception when importing modules in addon: %s" % format(e))
    sys.exit(1)

pkg_name_max_len = 30
pkg_version_max_len = 16

def update_configin():
    pass

def is_parent_dir(dir, dirs):
    # exclude the tailing '/' or '\'
    dir = str(dir)
    if dir.endswith(os.path.sep):
        dir = dir[:-1]

    for d in dirs:
        d = str(d)
        # exclude the tailing '/' or '\'
        if d.endswith(os.path.sep):
            d = d[:-1]

        if len(d) > len(dir) and d.startswith(dir):
            return True

    return False

def print_upgrade_list_header():
    aos_info("Package"+" "*(pkg_name_max_len-len("Package"))+
             "Old version"+" "*(pkg_version_max_len-len("Old version"))+
             "New version")
    aos_info("-"*(pkg_name_max_len+pkg_version_max_len*2))

class Cache():
    def __init__(self, repourl=None, cachedir=None):
        if not repourl:
            self.repourl = OS_REPO
        else:
            self.repourl = repourl

        if not cachedir:
            self.cachedir = OS_CACHE
        else:
            self.cachedir = cachedir

        self.primary_db_file = None
        self.filelists_db_file = None
        self.other_db_file = None
        self.comp_info_db_file = None
        self.primary_db = None
        self.filelists_db = None
        self.other_db = None
        self.comp_info_db = None
        self.repo = None

    def __del__(self):
        try:
            # delete database
            if self.primary_db_file:
                self.primary_db_file.close()
            if self.filelists_db_file:
                self.filelists_db_file.close()
            if self.other_db_file:
                self.other_db_file.close()

            # delete cache dir
            if os.path.isdir(self.cachedir):
                host_os = get_host_os()
                # strange, rmtree on windows sometimes results in folder busy error
                if False: #host_os == 'Win32':
                    #os.system('del /F ' + self.cachedir)
                    os.system('rm -fr ' + self.cachedir)
                else:
                    shutil.rmtree(self.cachedir)
        except Exception as e:
            debug("Failure when cache.__del__: %s" % format(e))
            pass

    def create(self):
        """ Create cache dir """
        if not os.path.isdir(self.cachedir):
            os.makedirs(self.cachedir)

        mdtypes = ["primary_db", "filelists_db", "other_db"]
        self.repo = repo.Repo(self.repourl, self.cachedir)
        r = self.repo
        r.getRepoFile()
        for mdtype in mdtypes:
            mdfile = r.getMDFile(mdtype)
            outfile = misc.decompress(mdfile)
            setattr(self, mdtype, outfile)

        self.comp_info_db = r.getCompInfoFile()

    def construct_repo_db(self):
        # TODO: Do we need construct all the databases on __init__?
        self.primary_db_file = sqlitedb.PrimaryDB(self.primary_db)
        self.filelists_db_file = sqlitedb.FilelistsDB(self.filelists_db)
        self.other_db_file = sqlitedb.OtherDB(self.other_db)

    def construct_comp_info_db(self):
        self.comp_info_db_file = sqlitedb.PrimaryDB(self.comp_info_db)

def get_pkg_full_name(name, version):
    return '-'.join([name, version, pkg_rpm_postfix])

class AddonManager():
    def __init__(self):
        self.testing_env = False
        self.cache = Cache()
        self.cache.create()
        self.cache.construct_repo_db()
        self.localpkg = localpkg.LocalPkg()
        self.querysvr = queryserver.QueryServer()
        pass

    def __del__(self):
        pass

    # Check if it's a valid wksp to do the add operations
    def _is_wksp_valid(self):
        if not self.localpkg.validate():
            return False
        else:
            return True

    # Get full packge information, either remote or local
    def _get_pkg_info(self, remote, names, pkgkey_required=False):
        pkgs_info = []

        # Get pkg dictionary
        if (remote):
            if QUERY_PKGLIST:
                osver = self.localpkg.getOsVersion()
                if not osver:
                    aos_error("Failed to fetch OS version information!")
                pkgs_info = self.querysvr.query_pkginfo(osver, names)
                if not pkgs_info:
                    aos_warning("No information found on server for "\
                                "AliOS Things version %s!" % osver)
                    return None
                if pkgkey_required:
                    pkgs_info = self.cache.primary_db_file.getPackagesWithVersion(names)
            else:
                pkgs_info = self.cache.primary_db_file.getPackagesWithVersion(names)
        else:
            if not self._is_wksp_valid():
                return None
            else:
                pkgs_info = self.localpkg.getPackagesWithVersion(True, names)

        return pkgs_info

    # Get version specific packge information, either remote or local
    def _get_versioned_pkg_info(self, remote, name_ver):
        ret = []

        if not name_ver:
            return []

        pkgs_info = self._get_pkg_info(remote, list(name_ver.keys()))
        if pkgs_info:
            for p in pkgs_info:
                if name_ver[p[pkg_name_in_dict]] == p[pkg_version_in_dict]:
                    ret.append(p)

        return ret

    def _get_versioned_pkg_info_with_pkgkey(self, remote, name_ver):
        ret = []

        if not name_ver:
            return []

        pkgs_info = self._get_pkg_info(remote, list(name_ver.keys()), pkgkey_required=True)
        if pkgs_info:
            for p in pkgs_info:
                if name_ver[p[pkg_name_in_dict]] == p[pkg_version_in_dict]:
                    ret.append(p)

        return ret

    # Remove the duplicate ones and retain the latest version
    def _refine_pkg_info_to_latest(self, pkgs_info):
        pkgs_info_new = []

        if not pkgs_info:
            return []

        # Remove duplddicated
        for item in pkgs_info:
            operation = "append"
            name = item[pkg_name_in_dict]
            version = item[pkg_version_in_dict]
            for i in pkgs_info_new:
                if name != i[pkg_name_in_dict]:
                    continue
                else:
                    if misc.version_greater_than(version, i[pkg_version_in_dict]):
                        operation = "replace"
                    else:
                        operation = "None"
                    # If match found, than no need continue to check
                    break

            # if no break, than need insert the new item
            if operation == "replace":
                pkgs_info_new.remove(i)
                pkgs_info_new.append(item)
            elif operation == "append":
                pkgs_info_new.append(item)

        # exclude board and mcu components
        '''
        for i in pkgs_info_new:
            name = i[pkg_name_in_dict]
            if name.startswith("board_") or name.startswith("mcu_") or name.startswith("mcu_"):
                pkgs_info_new.remove(i)
        '''

        return pkgs_info_new

    def _is_version_match(self, osver, pkgname, pkgver):
        # TODO
        vers = self.querysvr.query_ver(pkgname, osver)
        if pkgver in vers:
            return True
        else:
            return False

    def list(self, remote, showall, *arg):
        # List in below format:
        '''
        print format as below:
        Package                                Version
        -------------------------------------- --------
        soupsieve                              1.9
        tornado                                5.0.2
        urllib3                                1.22
        '''
        names = []

        if not self._is_wksp_valid():
            return -1

        for a in arg:
            names.append(a)

        pkgs_info = self._get_pkg_info(remote, names)

        if not pkgs_info:
            if remote:
                aos_warning("No component for this version of AliOS Things(%s) "\
                            "found on server." % self.localpkg.getOsVersion())
            return -1

        if not showall:
            pkgs_info_new = self._refine_pkg_info_to_latest(pkgs_info)
            pkgs_info = pkgs_info_new

        # Print the package infomation
        aos_print("Package"+" "*(pkg_name_max_len-len("package")+1)+"Version")
        aos_print('-'*pkg_name_max_len + ' ' + '-'*pkg_version_max_len)
        for item in pkgs_info:
            name = item[pkg_name_in_dict]

            # Do not list board or mcu components if not to show all
            if not showall:
                if name.startswith("board_") or \
                   name.startswith("mcu_") or \
                   name.startswith("arch_"):
                    continue

            version = item[pkg_version_in_dict]
            sys.stdout.write(name)
            sys.stdout.write(" "*(pkg_name_max_len-len(str(name))+1))
            sys.stdout.write(version)
            sys.stdout.write("\n")
            sys.stdout.flush()

        return 0

    # install specified components, and their dependencies (TODO)
    def install(self, force, dir, *arg):
        names = []

        if not self._is_wksp_valid():
            return

        for i in arg:
            names.append(i)

        if not dir and not names:
            aos_error("No component specified!")

        if dir: # install from provided file
            self._install_from_file(force, dir)
        else: # install from repo
            # find all local and remote kgs, used by multiple places
            all_remote_pkgs = self._get_pkg_info(True, [])
            if not all_remote_pkgs:
                aos_error("Terminated!")
            latest_remote_pkgs = self._refine_pkg_info_to_latest(all_remote_pkgs)
            all_old_pkgs = self.localpkg.getPackagesWithVersion(True, [])

            ret = 0
            if QUERY_DEP:
                ret = self._query_dep_from_remote_and_install(force, names, all_remote_pkgs,
                                                              latest_remote_pkgs, all_old_pkgs)
            else:
                ret = self._query_dep_from_local_and_install(force, names, all_remote_pkgs,
                                                             latest_remote_pkgs, all_old_pkgs)
            if ret != 0:
                aos_error("Installation terminated!")

    def _query_dep_from_remote_and_install(self, force, names, all_remote_pkgs, latest_remote_pkgs, all_old_pkgs):
        old_pkgs = []
        pkg_info = []
        pkg_info_new = []
        installed = []
        pkg_info_latest = {}
        pkg_to_install = {}
        deps = []
        missing_deps = {}
        ret = 0

        namelist = []
        localall = False

        # used to find pkgname in [{"pkgname":"pkgverson"},{},]
        nameinlist = lambda x,y:x

        for n in names:
            # Check local
            if not localall:
                if n.startswith('board_') or \
                   n.startswith('mcu_') or \
                   n.startswith('arch_'):
                    localall = True

            if not '=' in n:
                namelist.append(n)
            else:
                namelist.append(re.findall(r'(.+)=.+', n)[0])

        # find already installed pkgs
        already = []
        for p in all_old_pkgs:
            if p[pkg_name_in_dict] in namelist:
                already += ["%s=%s" % (p[pkg_name_in_dict], p[pkg_version_in_dict])]

        # If there is any installed version, warn user to take action
        if already:
            aos_warning("These components have been installed: " + 
                        ', '.join(str(x) for x in already))

            if not force:
                # TODO: handle newer version install in a more elegant way?
                err, choice = aos_input("Do you want to replace? type 'Y[es]' or 'N[o]': ")
                if err != 0:
                    aos_error("[Error] Something bad happended, let's exit!")
                choice = choice.strip()
                if not choice == "Yes" and not choice == "Y":
                    aos_info("Installation terminated!")
                    return 0
            else:
                aos_warning("You have chosen to replace the installed version. "
                        "Please make sure you know what is happening!!!")

        osver = self.localpkg.getOsVersion()
        if not osver:
            aos_error("Unknown AliOS Things version!")
            return -1

        # making {"pkgname":"pkgver"} dictionary
        for n in names:
            pkgname = None
            pkgver = None

            # Get package name and version information
            if "=" in n: # specified version
                pkgname = re.findall(r'(.+)=.+', n)[0]
                pkgver = re.findall(r'.+=(.+)', n)[0]

                if not pkgname or not pkgver:
                    aos_warning("Invalid component name or version specified: %s!" % format(n))
                    return -1

                if not self._is_version_match(osver, pkgname, pkgver):
                    aos_warning("No matching version of component %s=%s for OS version %s found." % (pkgname, pkgver, osver))
                    return -1
            else: # latest version
                vers = self.querysvr.query_ver(n, osver)
                if not vers:
                    aos_warning("No matching version found for pkg %s" % n)
                    return -1

                pkgname = n
                pkgver = vers[0]
                for v in vers:
                    if misc.version_greater_than(v, pkgver):
                        pkgver = v

            if pkgname not in pkg_to_install.keys():
                pkg_to_install[pkgname] = pkgver
            else:
                if misc.version_greater_than(pkgver, pkg_to_install[pkgname]):
                    pkg_to_install[pkgname] = pkgver

            # fetch dependency
            dep = self._get_dependency_from_remote(pkgname, pkgver)
            if not dep:
                continue

            # add missing dependency to install list
            for d in dep:
                if not d[DEP_NAME] in pkg_to_install.keys() and \
                   not d[DEP_NAME] in list((lambda x:x[DEP_NAME])(x) for x in deps):
                    deps.extend([d])

        sys.stdout.write("The following packages will be installed: ")
        for k,v in pkg_to_install.items():
            sys.stdout.write("%s=%s " % (k, v))
        sys.stdout.write("\n")
        sys.stdout.flush()

        # let user confirm the install list
        if not force:
            err, choice = aos_input("Continue to process? type 'Y[es]' or 'N[o]': ")
            choice = choice.strip()
            if not choice == 'Y' and not choice == 'Yes':
                aos_warning("Installation terminated!")
                return -1

        # find out more dependency
        new_deps = deps
        deps_missing = [] # content: [{"pkgname":"pkgver"},{},]
        deps_missing_names = [] # content: ["names", "name2"]
        deps_upgrade = [] # content: [{"pkgname":"pkgver"},{},]
        deps_upgrade_names = [] # content: ["names", "names"]
        deps_downgrade = [] # content: [{"pkgname":"pkgver"},{},]
        deps_downgrade_names = [] # content: ["names", "name2"]
        while len(new_deps) != 0:
            to_check = new_deps
            new_deps = []
            for d in to_check:
                state = 'missing'
                dname = d[DEP_NAME]
                dminver = d[DEP_VER_MIN]
                dmaxver = d[DEP_VER_MAX]

                # if maxver not provided, replace with latest ver
                if dmaxver == '0.0.0':
                    for p in latest_remote_pkgs:
                        if p[pkg_name_in_dict] == dname:
                            dmaxver = p[pkg_version_in_dict]
                            break

                # examine if it's a reasonable version number
                for p in all_old_pkgs:
                    pn = p[pkg_name_in_dict]
                    pv = p[pkg_version_in_dict]
                    if dname == pn:
                        if misc.version_greater_than(pv, dmaxver):
                            state = 'downgrade'
                        elif misc.version_greater_than(dminver, pv):
                            state = 'upgrade'
                        else:
                            state = 'useful'

                        break

                if state == 'useful':
                    to_add_ver = pv
                else:
                    to_add_ver = dmaxver

                to_add = dict(zip([dname], [to_add_ver]))
                if state == 'missing':
                    deps_missing.extend([to_add])
                    deps_missing_names.extend([dname])
                elif state == 'upgrade':
                    deps_upgrade.extend([to_add])
                    deps_upgrade_names.extend([dname])
                elif state == 'downgrade':
                    deps_downgrade.extend([to_add])
                    deps_downgrade_names.extend([dname])

                # remote result format: [{"name":"xxx", "min":"xxx", "max":xxx}, {},]
                dep = self._get_dependency_from_remote(dname, to_add_ver)
                # if not already in to_install list, add as new dependency
                for d in dep:
                    if d[DEP_NAME] in namelist or \
                       d[DEP_NAME] in deps_missing_names + deps_upgrade_names + deps_downgrade_names:
                        continue
                    else:
                        new_deps.extend([d])

        if not force:
            hint = False

            if deps_missing_names:
                hint = True
                aos_info("The follwoing dependency will be installed: %s" %
                         ', '.join(str(x) for x in deps_missing_names))
            if deps_upgrade_names:
                hint = True
                aos_info("The follwoing dependency will be upgraded: %s" %
                         ', '.join(str(x) for x in deps_upgrade_names))
            if deps_downgrade_names:
                hint = True
                aos_info("The follwoing dependency will be downgraded: %s" %
                         ', '.join(str(x) for x in deps_downgrade_names))

            if hint:
                err, choice = aos_input("Do you want to continue? type 'Y[es]' or 'N[o]': ")
                if err != 0:
                    aos_error("[Error] Something bad happended, let's exit!")

                choice = choice.strip()
                if not choice == "Yes" and not choice == "Y":
                    aos_info("Installation terminated!")
                    return 0
        else:
            aos_warning("You have chosen to replace the installed version. "
                    "Dependency will be upgraded or downgraded automatically!!!")

        # combine all to install into one dict
        for i in deps_missing:
            pkg_to_install.update(i)
        for i in deps_upgrade:
            pkg_to_install.update(i)
        for i in deps_downgrade:
            pkg_to_install.update(i)

        #pkg_to_install = dict(set(pkg_to_install))

        # find already installed pkgs
        already = []
        for p in all_old_pkgs:
            if p[pkg_name_in_dict] in pkg_to_install.keys():
                already += "%s" % p[pkg_name_in_dict]

        rpkg_info = self._get_pkg_info(True, list(pkg_to_install.keys()))
        if not rpkg_info:
            aos_error("Terminated!")

        for pkgname, pkgver in pkg_to_install.items():
            # Remove old first if any
            if pkgname in already:
                if self._uninstall(False, False, rpkg_info, [pkgname]) != 0:
                    aos_warning("Failed to uninstall old %s, new version"
                            " is not installed" % pkgname)
                    ret -= 1
                    continue

            # Download and install rpm
            rpmname = get_pkg_full_name(pkgname, pkgver)
            rpm = self.cache.repo.getPackage(rpmname)

            if not os.path.isfile(rpm):
                aos_warning("Failed to download pakcage, %s is not installed!" % pkgname)
                ret = -1
                continue

            r = rpmfile.RPMFile(rpm)
            r.install(self.localpkg.aos_src_root)

            # TODO: Update the related Config.in files
            update_configin()

            installed.append(pkgname)
            aos_info("Component %s=%s installed in %s" %
                     (pkgname, pkgver, self.localpkg.aos_src_root))

        aos_info("Component(s): '%s' installed" % ', '.join(str(x) for x in installed))
        not_installed = set(pkg_to_install.keys()) - set(installed)
        if not_installed:
            aos_warning("Not installed components: '%s'! Please redo "
                    "installation for them!" % ', '.join(str(x) for x in not_installed))

        return ret

    def _query_dep_from_local_and_install(self, force, names, all_remote_pkgs, latest_remote_pkgs, all_old_pkgs):
        old_pkgs = []
        pkg_info = []
        pkg_info_new = []
        installed = []
        pkg_info_latest = {}
        ret = 0

        namelist = []
        localall = False

        for n in names:
            # Check local
            if not localall:
                if n.startswith('board_') or \
                   n.startswith('mcu_') or \
                   n.startswith('arch_'):
                    localall = True

            if not '=' in n:
                namelist.append(n)
            else:
                namelist.append(re.findall(r'(.+)=.+', n)[0])

        old_pkgs = self.localpkg.getPackagesWithVersion(localall, namelist)

        # If there is any installed version, warn user to take action
        if old_pkgs:
            old_info = lambda d:d[pkg_name_in_dict]+'='+d[pkg_version_in_dict]
            aos_warning("These components have been installed: " + 
                    ', '.join(map(old_info, old_pkgs)))
            if not force:
                # TODO: handle newer version install in a more elegant way?
                err, choice = aos_input("Do you want to replace? type 'Y[es]' or 'N[o]': ")
                if err != 0:
                    aos_error("[Error] Something bad happended, let's exit!")
                choice = choice.strip()
                if not choice == "Yes" and not choice == "Y":
                    aos_info("Installation terminated!")
                    return 0
            else:
                aos_warning("You have chosen to replace the installed version. "
                        "Please make sure you know what is happening!!!")

        pkg_info = self._get_pkg_info(True, namelist)
        if not pkg_info:
            aos_error("Terminated!")
        pkg_info_namelist = [(lambda p:p[pkg_name_in_dict])(p) for p in pkg_info]
        missing_namelist = set(namelist) - set(pkg_info_namelist)
        if not pkg_info or len(missing_namelist):
            aos_error("Failed to get remote component information for '%s'" % 
                  ', '.join(missing_namelist))

        pkg_info_new = self._refine_pkg_info_to_latest(pkg_info)

        for pkg in pkg_info_new:
            pkg_info_latest[pkg[pkg_name_in_dict]] = pkg[pkg_version_in_dict]

        osver = self.localpkg.getOsVersion()
        if not osver:
            aos_warning("Unknown AliOS Things version!")
            return -1

        while len(names) > 0:
            n = names[0]
            pkgname = None
            pkgver = None

            # Get package name and version information
            if "=" in n: # specified version
                pkgname = re.findall(r'(.+)=.+', n)[0]
                pkgver = re.findall(r'.+=(.+)', n)[0]

                if not pkgname or not pkgver:
                    aos_warning("Invalid component name or version specified!")
                    ret -= 1
                    continue
            else: # latest version
                pkgname = n
                pkgver = pkg_info_latest[pkgname]

            # Check if the OS and pkg version match
            if not self._is_version_match(osver, pkgname, pkgver):
                aos_warning("Component %s=%s not installed! Not expected OS "
                        "version %s." % (pkgname, pkgver, osver))
                ret -= 1
                continue

            # Remove old first if any
            if pkgname in map(lambda p:p[pkg_name_in_dict], old_pkgs):
                if self._uninstall(False, False, pkg_info, [pkgname]) != 0:
                    aos_warning("Failed to uninstall old %s, new version"
                            " is not installed" % pkgname)
                    ret -= 1
                    continue

            # Download and install rpm
            rpmname = get_pkg_full_name(pkgname, pkgver)
            rpm = self.cache.repo.getPackage(rpmname)

            r = rpmfile.RPMFile(rpm)
            r.install(self.localpkg.aos_src_root)

            # TODO: Update the related Config.in files
            update_configin()

            installed.append(pkgname)
            aos_info("Component %s=%s installed in %s" %
                     (pkgname, pkgver, self.localpkg.aos_src_root))

            dep = self._get_dependency_from_local(pkgname)
            if dep:
                missing_dep = self._get_missing_pkg(dep)
                missing_dep = list(set(missing_dep) - set(names))
                aos_info("Missing dependency found when installing "
                         "%s: %s" % (pkgname, str(missing_dep)))
                if missing_dep:
                    missing_dep_info = self._get_pkg_info(True, missing_dep)
                    if not missing_dep_info:
                        aos_error("Terminated!")
                    missing_dep_info_new = self._refine_pkg_info_to_latest(missing_dep_info)
                    for pkg in missing_dep_info_new:
                        pkg_info_latest[pkg[pkg_name_in_dict]] = pkg[pkg_version_in_dict]
                    names.extend(missing_dep)

            names.remove(n)

        aos_info("Component(s): '%s' installed" % str(installed))
        not_installed = set(namelist) - set(installed)
        if not_installed:
            aos_warning("Not installed components: '%s'! Please redo "
                    "installation for them!" % str(not_installed))

        return ret

    # Uninstall specified components only, no dependency!
    def uninstall(self, force, all, *arg):
        ret = 0
        names = []
        uninstall_all = False

        if not self._is_wksp_valid():
            return -1

        for i in arg:
            names.append(i)

        if not names and not all:
            aos_warning("No component specified! Nothing happened!")
            return 0

        if not all:
            ret = self._uninstall(force, all, None, names)
        else:
            aos_warning("You are going to uninstall all components. Is it the expected operation?")
            err, choice = aos_input("Please confirm by typing 'Y[es]' or 'N[o]': ")
            if err != 0:
                aos_error("[Error] Something bad happended, let's exit!")
            choice = choice.strip()
            if choice == "Yes" or choice == "Y":
                uninstall_all = True
            else:
                aos_info("Operation terminated.")
                sys.exit(0)

        # Clean top level dirs
        if not self.testing_env and uninstall_all:
            for d in list(OS_COMPONENT_DIRS) + list(OS_PLATFORM_DIRS):
                d = os.path.join(self.localpkg.aos_src_root, d)
                # delete all subfolder and files in top level dirs, but keep top level dirs themselves.
                if not os.path.isdir(d):
                    continue
                for filename in os.listdir(d):
                    filepath = os.path.join(d, filename)
                    try:
                        if os.path.isfile(filepath) or os.path.islink(filepath):
                            os.unlink(filepath)
                        elif os.path.isdir(filepath):
                            shutil.rmtree(filepath)
                    except Exception as e:
                        aos_error("[Error] Failed to delete %s, error: %s" % (filepath, format(e)))

        if uninstall_all:
            aos_info("All components have been uninstalled.")

        return ret

    def _uninstall(self, force, all, rpkgs, names):
        old_pkgs = []
        uninstalled = []
        ret = 0

        if not names:
            return 0

        localall = None
        for n in names:
            # Check local
            if n.startswith('board_') or \
               n.startswith('mcu_') or \
               n.startswith('arch_'):
                localall = True
            if localall:
                break

        # Get local pkg name and list
        old_pkgs = self.localpkg.getPackagesWithVersion(localall, names)
        local_missing = set(names) - set(map(lambda x:x[pkg_name_in_dict], old_pkgs))
        if local_missing:
            aos_warning("The following specified components are not"
                    " installed: " + str(local_missing))
            aos_warning("Uninstall process terminated!")
            return -1

        # Get remote pkg info if not provided
        if not rpkgs:
            name_ver = {}
            for p in old_pkgs:
                name_ver[p[pkg_name_in_dict]] = p[pkg_version_in_dict]
            pkg_info = self._get_versioned_pkg_info_with_pkgkey(True, name_ver)
        else:
            pkg_info = rpkgs

        remote_missing = set(names) - set([(lambda p:p[pkg_name_in_dict])(p) for p in pkg_info])
        if remote_missing:
            aos_warning("The following specified components are "\
                        "not found on server: " + str(remote_missing))
            aos_warning("\nIf this is a component "\
                        "locally created or copied, you need remove it manually.")
            aos_warning("Uninstall process terminated!")
            return -1

        # Iterate on each pkg
        _sep = os.path.sep
        for pkg in pkg_info:
            failure = 0

            # Get remote filelist info according to pkgkey
            if not pkg_pkgkey_in_dict in pkg.keys():
                aos_error("pkgkey is missing in the pkg info!")
            pkgkey = pkg[pkg_pkgkey_in_dict]
            filelist_info = self.cache.filelists_db_file.getFiles(pkgkey)
            if not filelist_info:
                aos_warning("Failed to get information for package %s, "
                        "not uninstalled!" % pkg[pkg_name_in_dict])
                ret -= 1
                continue

            # Delete files, and dirs if become empty
            dirs = list(map(lambda x:x[pkg_dirname_in_dict], filelist_info))
            while len(filelist_info) > 0:
                i = filelist_info[0]
                terminated = False

                # if not leaf dir, iterate it later
                if is_parent_dir(i[pkg_dirname_in_dict], dirs):
                    filelist_info.remove(i)
                    filelist_info.append(i)
                    continue

                # delete files
                dir = self.localpkg.aos_src_root + i[pkg_dirname_in_dict]
                files = i[pkg_filenames_in_dict].split('/')
                for f in files:
                    file = _sep.join([dir, f])
                    if os.path.isfile(file):
                        try:
                            os.remove(file)
                        except Exception as e:
                            aos_warning("Failed to delete file %s (error: %s)" % (file, format(e)))
                            aos_warning("Component %s uninstall process terminated, please "
                                    "remove the directory %s manually!" % 
                                    (pkg[pkg_name_in_dict], dir))
                            terminated = True
                            break
                    else:
                        failure += 1
                        aos_print("Warning: invalid file %s" % file)

                if terminated:
                    dirs.remove(i[pkg_dirname_in_dict])
                    filelist_info.remove(i)
                    ret -= 1
                    continue

                # delete the dir if become empty or if only ucube.py left in it
                if os.path.isdir(dir):
                    _left = os.listdir(dir)
                    if not _left or (len(_left) == 1 and _left[0] == 'ucube.py'):
                        try:
                            shutil.rmtree(dir)
                        except Exception as e:
                            aos_warning("Failed to delete dirertory %s, error: %s" % (dir, format(e)))
                            aos_warning("Component %s uninstall process terminated, please "
                                    "remove the directory %s manually!" %
                                    (pkg[pkg_name_in_dict], dir))
                            dirs.remove(i[pkg_dirname_in_dict])
                            filelist_info.remove(i)
                            ret -= 1
                            continue

                    # delete parent dir if becom empty, this deals with the
                    # cases like xxx/yyy/zzz/a.txt, when a.txt is deleted,
                    # xxx, yyy, and zzz all become empty, thus xxx, yyy, zzz
                    # all should be deleted, not only zzz.
                    terminated = False
                    parent_dir = os.path.abspath(os.path.join(dir, ".."))
                    while is_parent_dir(self.localpkg.aos_src_root, [parent_dir]):
                        if not os.path.isdir(parent_dir) or os.listdir(parent_dir):
                            break

                        # delete this dir since it becomes empty now
                        try:
                            shutil.rmtree(parent_dir)
                        except Exception as e:
                            aos_warning("Failed to delete dirertory %s, error: %s" % (dir, format(e)))
                            aos_warning("Component %s uninstall process terminated, please "
                                    "remove the directory %s manually!" %
                                    (pkg[pkg_name_in_dict], dir))
                            terminated = True
                            break

                        parent_dir = os.path.abspath(os.path.join(parent_dir, ".."))

                    if terminated:
                        dirs.remove(i[pkg_dirname_in_dict])
                        filelist_info.remove(i)
                        ret -= 1
                        continue

                dirs.remove(i[pkg_dirname_in_dict])
                filelist_info.remove(i)

            # Update Config.in
            update_configin()

            if failure > 1:
                aos_warning("Failed to uninstall component %s\n"\
                            "Seems like something wrong with the local version of the component.\n"\
                            "Please make sure the version numbers are not modified unexpectly."\
                            % pkg[pkg_name_in_dict])
            else:
                uninstalled.append(pkg[pkg_name_in_dict])

        if uninstalled:
            aos_info("Component(s): '%s' uninstalled" % \
                     ', '.join(str(x) for x in uninstalled))

        not_uninstalled = set(names) - set(uninstalled)
        if not_uninstalled:
            aos_warning("Not uninstalled components: '%s'! Please redo the "
                    "uninstallation for them!" % str(not_uninstalled))

        return ret

    def upgrade(self, onlychk, *arg):
        names = []
        upgrade_list = []
        local_dict = {}
        remote_dict = {}

        if not self._is_wksp_valid():
            return -1

        for i in arg:
            names.append(i)

        local_pkgs = self._get_pkg_info(False, names)
        names = list((lambda x:x[pkg_name_in_dict])(p) for p in local_pkgs)
        remote_pkgs = self._get_pkg_info(True, names)
        if not remote_pkgs:
            aos_error("Terminated!")
        remote_pkgs = self._refine_pkg_info_to_latest(remote_pkgs)
        remote_names = list((lambda x:x[pkg_name_in_dict])(p) for p in remote_pkgs)

        if not local_pkgs:
            aos_info("No component is installed.")
            return 0

        missing_names = None
        local_pkgs_new = []
        if len(local_pkgs) != len(remote_pkgs):
            #aos_warning("local (len=%d): %s\n\nremote(len=%d): %s" % \
            #            (len(local_pkgs), str(local_pkgs), \
            #            len(remote_pkgs), str(remote_pkgs)))
            missing_names = list(set(names) - set(remote_names))
            aos_warning("Some component(s) cannot be found on remote server: %s\n"
                        "Only the found components will be upgraded.\n" %
                        ', '.join(str(x) for x in missing_names))
            err, choice = aos_input("Do you want to continue? type 'Y[es]' or 'N[o]': ")
            if err != 0:
                aos_warning("Error happened!")
                return -1
            else:
                choice = choice.strip()
                if choice == "Y" or choice == "Yes":
                    # exclude remote missing pkgs
                    for i in local_pkgs:
                        if i[pkg_name_in_dict] in remote_names:
                            new_local_names = list((lambda x:x[pkg_name_in_dict])(p) for p in local_pkgs_new)
                            if i[pkg_name_in_dict] in new_local_names:
                                # hack for publish components, which may exist in internal test
                                if i[pkg_localdir_in_dict].endswith('publish') or \
                                   i[pkg_localdir_in_dict].endswith('publish' + os.path.sep):
                                    aos_warning("In upgrade(), seems like component %s(in %s) "\
                                                "is not a valid component, will ignore it." %\
                                                (i[pkg_name_in_dict], i[pkg_localdir_in_dict]))
                                continue
                            local_pkgs_new += [i]
                else:
                    aos_info("Upgrade process terminated!")
                    return 0

        if local_pkgs_new:
            local_pkgs = local_pkgs_new

        if len(local_pkgs) != len(remote_pkgs):
            aos_error("local(len=%d) mismatch remote(len=%d)!" %
                      (len(local_pkgs), len(remote_pkgs)))

        k = lambda s:s[pkg_name_in_dict]
        local_pkgs.sort(key=k)
        remote_pkgs.sort(key=k)

        _upgrade_header_print = False
        for i in range(len(local_pkgs)):
            if local_pkgs[i][pkg_version_in_dict] < remote_pkgs[i][pkg_version_in_dict]:
                name = local_pkgs[i][pkg_name_in_dict]
                old_version = local_pkgs[i][pkg_version_in_dict]
                new_version = remote_pkgs[i][pkg_version_in_dict]

                if onlychk:
                    # header print if not already
                    if not _upgrade_header_print:
                        print_upgrade_list_header()
                        _upgrade_header_print = True

                    # print pkg name and version information
                    sys.stdout.write(name)
                    sys.stdout.write(" "*(pkg_name_max_len-len(str(name))))
                    sys.stdout.write(old_version)
                    sys.stdout.write(" "*(pkg_version_max_len-len(str(old_version))))
                    sys.stdout.write(new_version)
                    sys.stdout.write("\n")
                    sys.stdout.flush()

                upgrade_list.append(name+'='+new_version)

        if not upgrade_list:
            aos_info("Everything is up-to-date.")
        elif not onlychk:
            aos_print("The following packages as well as their dependency will be installed: ")
            for u in upgrade_list:
                aos_print("%s " % u)
            aos_print("\n")

            err, choice = aos_input("Do you want to continue? type 'Y[es]' or 'N[o]': ")
            if err != 0:
                aos_warning("Error happened!")
                return -1
            else:
                choice = choice.strip()
                if choice == "Y" or choice == "Yes":
                    self.install(True, None, *tuple(upgrade_list))

        return 0

    def _get_dependency_from_local(self, pkgname):
        return self.localpkg.getDependency(pkgname)

    def _get_dependency_from_remote(self, pkgname, pkgver):
        return self.querysvr.query_dep(pkgname, pkgver)

    def _get_missing_pkg(self, pkgnames):
        return self.localpkg.getMissingPackages(pkgnames)

    def _get_missing_versioned_pkg(self, pkgs):
        return self.localpkg.getMissingVersionedPackages(pkgs)

    # Create a component with files from 'dir', and zip result placed in cur dir
    def create(self, dir):
        srcdir = dir

        if not self._is_wksp_valid():
            return -1

        if not os.path.isabs(dir):
            srcdir = os.path.abspath(dir)

        rootdir = self.localpkg.aos_src_root
        tmpdir = self.cache.cachedir
        dstdir = os.getcwd()
        srcdir_rel = os.path.relpath(srcdir, start=rootdir)
        firstlevelfolder = re.findall(r'^([0-9a-zA-Z\._\- ]+).*', srcdir_rel)
        if not firstlevelfolder:
            aos_error("Invalid dir provided!")
        else:
            firstlevelfolder = firstlevelfolder[0]

        # whether or not a valid component dir?
        if not (os.path.isfile(os.path.join(srcdir, 'aos.mk'))):
            aos_error("Not a valid component directory!")

        # find the name and version
        name = None
        version = None
        with open(os.path.join(srcdir, 'aos.mk'), 'r') as f:
            data = f.read().splitlines()
            for line in data:
                # match name
                if not name and re.findall(r'^\s*NAME\s*:?=.+', line):
                    pkgname = re.findall(r'.*=\s*(\S+)', line)
                    if pkgname:
                        name = pkgname[0]
                if not version and re.findall(r'^.*\$\(NAME\)_VERSION\s*:?=.+', line):
                    pkgver = re.findall(r'.*=\s*(\S+)', line)
                    if pkgver:
                        version = pkgver[0]
                        break

        if not name or not version:
            aos_error("Name or version missing in the component makefile!")

        # make the dir and copy the contents
        newtopdir = os.path.join(tmpdir, firstlevelfolder)
        try:
            if os.path.exists(newtopdir):
                shutil.rmtree(newtopdir)
            #os.makedirs(os.path.join(tmpdir, srcdir_rel))
            shutil.copytree(srcdir, os.path.join(tmpdir, srcdir_rel))
        except Exception as e:
            if os.path.exists(newtopdir):
                shutil.rmtree(newtopdir)
            aos_error("Failed to create (error: %s)!" % format(e))

        # zip the tmpdir
        zipf = os.path.join(tmpdir, '-'.join([name, version]) + '.zip')
        try:
            # zip, include only relative path
            os.chdir(tmpdir)
            with zipfile.ZipFile(zipf, 'w', zipfile.ZIP_DEFLATED) as myzip:
                for path, dirnames, filenames in os.walk(os.path.join(tmpdir, srcdir_rel)):
                    for file in filenames:
                        myzip.write(os.path.join(os.path.relpath(path, start=tmpdir), file))

            # copy to destination dir
            shutil.copy(zipf, dstdir)
        except Exception as e:
            if os.path.exists(newtopdir):
                shutil.rmtree(newtopdir)
            if os.path.exists(zipf):
                os.remove(zipf)
            aos_error('Failed to write to zip file (error: %s)' % format(e))

        aos_info("Component successfully created in %s" %
                 os.path.join(dstdir, '-'.join([name, version]) + '.zip'))

        return 0

    def _install_from_file(self, force, file):
        ''' TODO:
        handle force later, force will check if already installed
        and take action only if user want to replace the installed.
        '''
        if not dir:
            aos_warning("No component file provided!")
            return -1

        if not os.path.isfile(file):
            aos_warning("Not a valid file provided!")
            return -1

        file = os.path.abspath(file)
        if zipfile.is_zipfile(file):
            self._install_from_zip(file)
        elif file.endswith(".rpm"):
            r = rpmfile.RPMFile(file)
            r.install(self.localpkg.aos_src_root)
        else:
            aos_warning("Seems not a valid local component file, only .zip and .rpm file accepted!")
            return -1

        # TODO: Update the related Config.in files
        update_configin()

        aos_info("Local component %s is installed." % file)

        return 0

    # Only file itself is installed, not as well as its dependency.
    def _install_from_zip(self, file):
        if not file:
            return

        ''' TODO:
        1. check there is a valid component in the zip file.
        2. check if there is already an existing one.
        '''

        origdir = os.getcwd()

        try:
            os.chdir(self.localpkg.aos_src_root)
            rootdir = os.getcwd()
            with zipfile.ZipFile(file, "r") as myzip:
                badcrc = myzip.testzip()
                if badcrc:
                    aos_error("Bad CRC for file %s of the zip archive" % badcrc)

                myzip.extractall(rootdir)
        except Exception as e:
            aos_error("Failed to install from zip file, error: %s!" % format(e))
        finally:
            os.chdir(origdir)
