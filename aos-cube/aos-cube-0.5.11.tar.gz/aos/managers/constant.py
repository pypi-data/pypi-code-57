from aos.constant import AOS_SERVER_URL, AOS_HTTP_HEADER, AOS_HTTP_METHOD

'''
aos addon commands is only supported starting from ADDON_OS_VER_BASE.
old versions are not supported!
'''
ADDON_OS_VER_BASE = '3.1.0'

'''
AliOS Things source directory check points
'''
aos_src_dir_chk1 = 'include/aos'
aos_src_dir_chk2 = 'core'
aos_src_dir_chk3 = 'components'

'''
getPackagesxxx() in localpkg.py and sqlite.py will return a list of components.

Information in the list are as below:

    [
        {
            "name": "<comp_name1>",       # required
            "version": "<comp_version1>", # required
            # optional hereafter
            "pkgKey": <comp_pkgkey1>,     # used by remote list, optional for local
            "localdir": "<comp_dir1>",    # used by local list, not applicable for remote
            ...
        },
        ...
    ]
'''

pkg_name_in_dict = "name"
pkg_version_in_dict = "version"
pkg_localdir_in_dict = "localdir"
pkg_pkgkey_in_dict = "pkgKey"

'''
getFiles will return a list of file/dir information in below format:
    [
        {
            "pkgKey": "pkgkey1"
            "dirname": "dir1",
            "filenames": "filenames1"
        },
        ...
    ]
'''
pkg_dirname_in_dict = "dirname"
pkg_filenames_in_dict = "filenames"

'''
This is the postfix of the RPM file in repo.

RPM file name convention: <comp_name>-<comp_ver>-<rpm postfix>

    e.g.:

        activation-1.0.0-r0.aos.noarch.rpm
        arch_armv7a-1.0.1-r0.aos.noarch.rpm
        board_asr5501-1.0.0.1-r0.aos.noarch.rpm
        mcu_moc108-1.0.1.2-r0.aos.noarch.rpm
        zlib-1.0.0-r0.aos.noarch.rpm

'''
pkg_rpm_postfix = 'r0.aos.noarch.rpm'

pkg_name_board_prefix = "board_"
pkg_name_mcu_prefix = "mcu_"
pkg_name_arch_prefix = "arch_"

'''
Directories used for search components.

    OS_COMPONENT_DIRS: normal AliOS Things provided componets
    OS_PLATFORM_DIRS: 3rd party components

'''
OS_COMPONENT_DIRS = (["components", "application", "core"])
OS_PLATFORM_DIRS = (["platform"])

# Components version/dependency information http query servers
## general
PKG_QUERY_URL = AOS_SERVER_URL
PKG_QUERY_HTTP_HEADER = AOS_HTTP_HEADER
PKG_QUERY_HTTP_METHOD = AOS_HTTP_METHOD
## ver query
PKG_VER_QUERY_API = "/getComponentVersionOfSystemVersion"
PKG_VER_QUERY_DATA_FORMAT = "{\"compName\": \"%s\", \"systemVersion\":\"%s\"}"
## dep qeury
PKG_DEP_QUERY_API = "/getComponentDependency"
PKG_DEP_QUERY_DATA_FORMAT = "{\"name\": \"%s\", \"version\":\"%s\"}"
## comp list qeury
PKG_CLIST_QUERY_API = "/getComponentListOfSystemVersion"
PKG_CLIST_QUERY_DATA_FORMAT = "{\"systemVersion\":\"%s\"}"

# Wether query dependency from remote server through HTTP api
QUERY_DEP = True
# Wether query pkg info list from remote server through HTTP api
QUERY_PKGLIST = True

# dependency query results from remote provides in below format:
# a list of dict {"min":'x.x.x[.x]', "max":'x.x.x[.x]', "name":'xxx'}
DEP_NAME = "name"
DEP_VER_MIN = "min"
DEP_VER_MAX = "max"

# use urlgrabber or requests as url pakcage, urlgrabber is not likely to be
# good choice, will switch to requests later.
PYURLPKG = 'requests' # 'urlgrabber'
