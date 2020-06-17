import os

# Default paths to Mercurial and Git
hg_cmd = 'hg'
git_cmd = 'git'

ignores = [
    "make",
    "make.exe",
    "Makefile",
    "build",
    ".cproject",
    ".gdbinit",
    ".openocd_cfg",
    ".project",
    "aos",
    ".aos",
]

toolchains = {
    'arm-none-eabi':{
        'name': 'gcc-arm-none-eabi',
        'path': 'build/compiler/gcc-arm-none-eabi',
        'command': 'arm-none-eabi-gcc',
        'version': 'all',
        'use_global': True,
        'Win32_url':'https://gitee.com/alios-things/gcc-arm-none-eabi-win32.git',
        'Linux32_url': 'https://gitee.com/alios-things/gcc-arm-none-eabi-linux.git',
        'Linux64_url': 'https://gitee.com/alios-things/gcc-arm-none-eabi-linux.git',
        'OSX_url': 'https://gitee.com/alios-things/gcc-arm-none-eabi-osx.git',
        },
    'xtensa-esp32':{
        'name': 'gcc-xtensa-esp32',
        'path': 'build/compiler/gcc-xtensa-esp32',
        'command': 'xtensa-esp32-elf-gcc',
        'version': '5.2.0',
        'use_global': True,
        'Win32_url': 'https://gitee.com/alios-things/gcc-xtensa-esp32-win32.git',
        'Linux32_url': 'https://gitee.com/alios-things/gcc-xtensa-esp32-linux.git',
        'Linux64_url': 'https://gitee.com/alios-things/gcc-xtensa-esp32-linux.git',
        'OSX_url': 'https://gitee.com/alios-things/gcc-xtensa-esp32-osx.git',
        },
    'xtensa-lx106':{
        'name': 'gcc-xtensa-lx106',
        'path': 'build/compiler/gcc-xtensa-lx106',
        'command': 'xtensa-lx106-elf-gcc',
        'version': '4.8.2',
        'use_global': True,
        'Win32_url': 'https://gitee.com/alios-things/gcc-xtensa-lx106-win32.git',
        'Linux32_url': 'https://gitee.com/alios-things/gcc-xtensa-lx106-linux.git',
        'Linux64_url': 'https://gitee.com/alios-things/gcc-xtensa-lx106-linux.git',
        'OSX_url': 'https://gitee.com/alios-things/gcc-xtensa-lx106-osx.git',
        },
    'csky-abiv2': {
        'name': 'gcc-csky-abiv2',
        'path': 'build/compiler/gcc-csky-abiv2',
        'command': 'csky-abiv2-elf-gcc',
        'version': 'all',
        'use_global': True,
        'Win32_url': 'https://gitee.com/alios-things/gcc-csky-abiv2-win32.git',
        'Linux32_url': 'https://gitee.com/alios-things/gcc-csky-abiv2-linux.git',
        'Linux64_url': 'https://gitee.com/alios-things/gcc-csky-abiv2-linux.git',
        'OSX_url': '',
        },

    'arm-rockchip-linux-gnueabihf': {
        'name': 'gcc-arm-rockchip-linux-gnueabihf',
        'path': 'build/compiler/usr',
        'path_specific': True,
        'command': 'arm-rockchip-linux-gnueabihf-gcc',
        'version': 'all',
        'use_global': True,
        'Win32_url': '',
        'Linux32_url': 'https://gitee.com/alios-things/arm-rockchip-linux-gnueabihf-linux.git',
        'Linux64_url': 'https://gitee.com/alios-things/arm-rockchip-linux-gnueabihf-linux.git',
        'OSX_url': '',
        },

    'nds32le-elf-newlib-v3': {
        'name': 'nds32le-elf-newlib-v3',
        'path': 'build/compiler/nds32le-elf-newlib-v3',
        'path_specific': True,
        'command': 'nds32le-elf-gcc',
        'version': 'all',
        'use_global': True,
        'Win32_url': '',
        'Linux32_url': 'https://gitee.com/alios-things/gcc-nds32le-linux.git',
        'Linux64_url': 'https://gitee.com/alios-things/gcc-nds32le-linux.git',
        'OSX_url': '',
        },

    'openocd': {
        'name': 'OpenOCD',
        'path': 'build/OpenOCD',
        'command': 'openocd',
        'version': '0.10.0',
        'use_global': False,
        'Win32_url': 'https://gitee.com/alios-things/openocd-win32.git',
        'Linux32_url': '',
        'Linux64_url': 'https://gitee.com/alios-things/openocd-linux64.git',
        'OSX_url': 'https://gitee.com/alios-things/openocd-osx.git',
    }
}

boards = {
'amebaz_dev':[toolchains['arm-none-eabi']],
'atsame54-xpro':[toolchains['arm-none-eabi']],
'b_l475e':[toolchains['arm-none-eabi']],
'bk7231devkitc':[toolchains['arm-none-eabi']],
'bk7231udevkitc':[toolchains['arm-none-eabi']],
'bk3435devkit':[toolchains['arm-none-eabi']],
'developerkit':[toolchains['arm-none-eabi']],
'eml3047':[toolchains['arm-none-eabi']],
'esp32devkitc':[toolchains['xtensa-esp32']],
'esp8266':[toolchains['xtensa-lx106']],
'frdmkl27z':[toolchains['arm-none-eabi']],
'hobbit1_evb':[toolchains['csky-abiv2']],
'dh5021a_evb':[toolchains['csky-abiv2']],
'cb2201':[toolchains['csky-abiv2']],
'lpcxpresso54102':[toolchains['arm-none-eabi']],
'mk1101':[toolchains['arm-none-eabi']],
'mk3060':[toolchains['arm-none-eabi']],
'mk3080':[toolchains['arm-none-eabi']],
'mk3165':[toolchains['arm-none-eabi']],
'mk3166':[toolchains['arm-none-eabi']],
'mk3239':[toolchains['arm-none-eabi']],
'pca10056':[toolchains['arm-none-eabi']],
'pca10040':[toolchains['arm-none-eabi']],
'starterkit':[toolchains['arm-none-eabi']],
'stm32f769i-discovery':[toolchains['arm-none-eabi']],
'stm32f412zg-nucleo':[toolchains['arm-none-eabi']],
'stm32l073rz-nucleo':[toolchains['arm-none-eabi']],
'stm32l432kc-nucleo':[toolchains['arm-none-eabi']],
'stm32l433rc-nucleo':[toolchains['arm-none-eabi']],
'stm32l476rg-nucleo':[toolchains['arm-none-eabi']],
'stm32l496g-discovery':[toolchains['arm-none-eabi']],
'sv6266_evb':[toolchains['nds32le-elf-newlib-v3']],
'msp432p4111launchpad':[toolchains['arm-none-eabi']],
'xr871evb':[toolchains['arm-none-eabi']],
'rk1108':[toolchains['arm-rockchip-linux-gnueabihf']],
'uno-91h':[toolchains['arm-none-eabi']],
'ch6121evb':[toolchains['arm-none-eabi']],
'tg7100b':[toolchains['arm-none-eabi']],
}

# verbose logging
verbose = False
very_verbose = False
install_requirements = True
cache_repositories = True

# stores current working directory for recursive operations
cwd_root = ""

APP_PATH = 'app_path'
PROGRAM_PATH = 'program_path'
AOS_SDK_PATH = 'AOS_SDK_PATH'
OS_PATH = 'os_path'
OS_NAME = 'AliOS-Things'
PATH_TYPE = 'path_type'
AOS_COMPONENT_BASE_URL = 'https://github.com/AliOS-Things'
CUBE_MAKEFILE = 'cube.mk'
CUBE_MODIFY = 'cube_modify'
REMOTE_PATH = 'remote'
OS_CONFIG = "project.ini"
COMP_INFO_DB_FILE = "component_info_publish.db"
OS_REPO = "http://116.62.245.240/AliOSThings-2-packages/"
#OS_REPO = "http://11.238.148.13:81/2_test/"
OS_CACHE = os.path.join(os.path.expanduser("~"), ".aoscache")
OS_DEF_COMPS = [ "buildsystem", "system_include"]

# aos ota config
OTA_SERVER = "116.62.245.240"
OTA_EMQ_PORT = 17173
OTA_EMQ_TOKEN = "QWxpT1MtVGhpbmdzLXVkZXZ8dWRldiFAIyQl"
OTA_WEBSERVER_PORT = 7001
OTA_UDEBUG_LIB = 'udev.a'

# Path to scripts in OS
CHECK_WRAPPER = os.path.sep.join(["build", "check", "check_wrapper.py"])
GEN_SAL_STAGING = os.path.sep.join(["build", "scripts", "gen_sal_staging.py"])
GEN_MAL_STAGING = os.path.sep.join(["build", "scripts", "gen_mal_staging.py"])
GEN_NEWPROJECT = os.path.sep.join(["build", "scripts", "gen_newproject.py"])
GEN_APPSOURCE = os.path.sep.join(["build", "scripts", "gen_appsource.py"])
GEN_NEW_COMPONENT = os.path.sep.join(["build", "scripts", "gen_new_component.py"])

# App config
APP_CONFIG = ".aos"
APP_UPDATE_MKFILE = os.path.sep.join(["build", "scripts", "app_update_aosmk.py"])
APP_GEN_INCLUDES = os.path.sep.join(["build", "scripts", "app_gen_comp_index.py"])
APP_INCLUDES = "aos_comp_index.json"

# File to store user's choice of whether ot nor to participate in the tool improve plan.
AOS_INVESTIGATION_FILE = os.path.join(os.path.expanduser("~"), ".aos", ".ucubeplan")

# AOS query/report server
AOS_SERVER_URL = "https://os-activation.iot.aliyun.com/cube"
AOS_HTTP_HEADER = "Content-Type:application/json"
AOS_HTTP_METHOD = "POST"

# print debug message or not, bool value
DEBUG_PRINT = False

# No SDK/SRC messages, widely used
_HINT_COMMON = "No AliOS Things source directory found. To make things work, please:\n\n"
_SET_SDK_HINT =  "-> Set AOS_SDK_PATH environment variable to a valid\n"\
                 "   AliOS-Things source directory as below:\n\n"\
                 "     * Linux/MacOS/Git-Bash:\n"\
                 "         $ export AOS_SDK_PATH=<path_to_AliOS_Things_src>\n"\
                 "     * Windows CMD:\n"\
                 "         > set AOS_SDK_PATH=<path_to_AliOS_Things_src>\n\n"\
                 "   Please set it on system level if you want so.\n"
_RUN_INSIDE_SDK_HINT = "-> Run this command in AliOS Things source directory.\n"
NO_SDK_HINT = _HINT_COMMON + _SET_SDK_HINT
NOT_INSIDE_SDK_HINT = _HINT_COMMON + _RUN_INSIDE_SDK_HINT
NO_AOSSRC_HINT = _HINT_COMMON + _RUN_INSIDE_SDK_HINT + "\nOr,\n\n" + _SET_SDK_HINT
