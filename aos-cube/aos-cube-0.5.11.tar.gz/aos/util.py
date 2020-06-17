import contextlib
import os
import sys
import shutil
import stat
import subprocess
import platform
import re
import sys
import locale
from aos.constant import APP_CONFIG
import errno
from aos.constant import *

# Directory navigation
@contextlib.contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)


def relpath(root, path):
    return path[len(root) + 1:]


def staticclass(cls):
    for k, v in list(cls.__dict__.items()):
        if hasattr(v, '__call__') and not k.startswith('__'):
            setattr(cls, k, staticmethod(v))

    return cls


# Logging and output
def debug(msg):
    if DEBUG_PRINT:
        sys.stdout.write("%s\n" % msg)
        sys.stdout.flush()

def log(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


def message(msg):
    return "[AliOS-Things] %s\n" % msg


def info(msg, level=1):
    if level <= 0 or verbose:
        for line in msg.splitlines():
            log(message(line))


def action(msg):
    for line in msg.splitlines():
        log(message(line))


def warning(msg):
    for line in msg.splitlines():
        sys.stderr.write("[AliOS-Things] WARNING: %s\n" % line)
    sys.stderr.write("---\n")
    sys.stderr.flush()


def error(msg, code=-1):
    from aos.usertrace.do_report import report_op, set_op
    for line in msg.splitlines():
        sys.stderr.write("[AliOS-Things] ERROR: %s\n" % line)
    sys.stderr.write("---\n")
    sys.stderr.flush()
    res = 'fail: ' + msg
    set_op(result=res)
    report_op()
    sys.exit(code)

def simple_error(msg, code=-1):
    from aos.usertrace.do_report import report_op, set_op
    report_str = ''
    for line in msg.splitlines():
        sys.stderr.write("%s\n" % line)
    sys.stderr.write("---\n")
    res = 'fail: ' + msg
    set_op(result=res)
    report_op()
    sys.exit(code)

def aos_input(prompt):
    ret = 0
    answer = ''
    pyver = sys.version_info
    if pyver[0] < 3:
        try:
            if prompt:
                sys.stdout.write(prompt)
                sys.stdout.flush()
            answer = raw_input()
        except Exception as e:
            ret, answer = -1, ''
        return ret, answer
    elif pyver[0] >= 3:
        try:
            if prompt:
                sys.stdout.write(prompt)
                sys.stdout.flush()
            answer = input()
        except Exception as e:
            ret, answer = -1, ''
        return ret, answer
    else:
        warning("Not supported python version!")
        return -1, ''


def progress_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


progress_spinner = progress_cursor()


def progress():
    sys.stdout.write(next(progress_spinner))
    sys.stdout.flush()
    sys.stdout.write('\b')


# Process execution
class ProcessException(Exception):
    pass


def rmtree_readonly(directory):
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(directory, onerror=remove_readonly)


def popen(command, suppress_error=None, stdin=None, **kwargs):
    # command may be a single string command or list
    if isinstance(command, list):
        command_line = command
        newcmd = []
        for c in command:
            if not isinstance(c, str):
                newcmd += [c.encode(get_locale())]
            else:
                newcmd += [c]
    else:
        command_line = command.split()
        if not isinstance(command, str):
            command = command.encode(get_locale())
        newcmd = command

    info('Exec "' + ' '.join(command_line) + '" in ' + locale_to_unicode(os.getcwd()))

    try:
        proc = subprocess.Popen(newcmd, **kwargs)
    except OSError as e:
        if e[0] == errno.ENOENT:
            error(
                "Could not execute \"%s\".\n"
                "Please verify that it's installed and accessible from your current path by executing \"%s\".\n" % (
                command_line[0], command_line[0]), e[0])
        else:
            raise e

    if proc.wait() != 0:
        if not suppress_error:
            raise ProcessException(proc.returncode, command_line[0], ' '.join(command_line), os.getcwd())

    return proc.returncode


def pquery(command, stdin=None, **kwargs):
    # command may be a single string command or list
    if isinstance(command, list):
        command_line = command
        newcommand = []
        for c in command:
            if not isinstance(c, str):
                newcommand += [c.encode(get_locale())]
            else:
                newcommand += [c]
    else:
        if not isinstance(command, str):
            command = command.encode(get_locale())
        newcommand = command
        command_line = command.split()

    if very_verbose:
        info('Query "' + ' '.join(newcommand) + '" in ' + locale_to_unicode(os.getcwd()))
    try:
        proc = subprocess.Popen(newcommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    except OSError as e:
        if e[0] == errno.ENOENT:
            error(
                "Could not execute \"%s\".\n"
                "Please verify that it's installed and accessible from your current path by executing \"%s\".\n" % (
                command_line[0], command_line[0]), e[0])
        else:
            raise e

    stdout, _ = proc.communicate(stdin)

    if very_verbose:
        log(str(stdout).strip() + "\n")

    if proc.returncode != 0:
        raise ProcessException(proc.returncode, command_line[0], ' '.join(command_line), os.getcwd())

    return stdout

def pqueryerr(command, stdin=None, **kwargs):
    """ Run command and return err """
    # command may be a single string command or list
    if isinstance(command, list):
        command_line = command
        newcommand = []
        for c in command:
            if not isinstance(c, str):
                newcommand += [c.encode(get_locale())]
            else:
                newcommand += [c]
    else:
        command_line = command.split()
        if not isinstance(command, str):
            command = command.encode(get_locale())
        newcommand = command

    if very_verbose:
        info('Exec "' + ' '.join(newcommand) + '" in ' + locale_to_unicode(os.getcwd()))
    try:
        proc = subprocess.Popen(newcommand, stderr=subprocess.PIPE, **kwargs)
    except OSError as e:
        if e[0] == errno.ENOENT:
            error(
                "Could not execute \"%s\".\n"
                "Please verify that it's installed and accessible from your current path by executing \"%s\".\n" % (
                command_line[0], command_line[0]), e[0])
        else:
            raise e

    stdout, err = proc.communicate(stdin)

    if very_verbose:
        log(str(err).strip() + "\n")

    return proc.returncode, err

def exec_cmd(command, suppress_error=None, stdin=None, **kwargs):
    """ Run command and return output, errcode """
    # command may be a single string command or list
    if isinstance(command, list):
        command_line = command
        newcommand = []
        for c in command:
            if not isinstance(c, str):
                newcommand += [c.encode(get_locale())]
            else:
                newcommand += [c]
    else:
        command_line = command.split()
        if not isinstance(command, str):
            command = command.encode(get_locale())
        newcommand = command

    info('Exec "' + ' '.join(newcommand) + '" in ' + locale_to_unicode(os.getcwd()))

    try:
        proc = subprocess.Popen(newcommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except OSError as e:
        if e[0] == errno.ENOENT:
            error(
                "Could not execute \"%s\".\n"
                "Please verify that it's installed and accessible from your current path by executing \"%s\".\n" % (
                command_line[0], command_line[0]), e[0])
        else:
            raise e

    output, err = proc.communicate()
    if proc.wait() != 0:
        if not suppress_error:
            raise ProcessException(proc.returncode, command_line[0], ' '.join(command_line), os.getcwd())

    return output, err

def get_country_code():
    import requests
    import json
    url = "https://geoip-db.com/json"
    try:
        res = requests.get(url, timeout = 5)
        data = json.loads(res.text)
        return data['country_code']
    except Exception:
        return 'CN'

def is_domestic():
    if get_country_code() == 'CN':
        return True
    else:
        return False

def get_host_os():
    host_os = platform.system()
    if host_os == 'Windows':
        host_os = 'Win32'
    elif host_os == 'Linux':
        if platform.machine().endswith('64'):
            bit = '64'
        else:
            bit = '32'
        host_os += bit
    elif host_os == 'Darwin':
        host_os = 'OSX'
    else:
        host_os = None
    return host_os

def get_aos_url():
    """Figure out proper URL for downloading AliOS-Things."""
    if is_domestic():
        aos_url = 'https://gitee.com/alios-things/AliOS-Things.git'
    else:
        aos_url = 'https://github.com/alibaba/AliOS-Things.git'

    return aos_url

def cd_aos_root():
    original_dir = os.getcwd()
    host_os = get_host_os()
    if host_os == 'Win32':
        sys_root = re.compile(r'^[A-Z]{1}:\\$')
    else:
        sys_root = re.compile('^/$')
    while os.path.isdir('./include/aos') == False and os.path.isdir('./kernel/rhino') == False \
        and os.path.isdir('./include/core') == False and os.path.isdir('./core/rhino') == False \
        and os.path.isdir('./kernel/include/aos') == False and os.path.isdir('./kernel/core/rhino') == False:
        if sys_root.match(os.getcwd()):
            return 'fail', original_dir
        os.chdir('../')
    return 'success', original_dir

def cd_app_root():
    original_dir = os.getcwd()
    host_os = get_host_os()
    if host_os == 'Win32':
        sys_root = re.compile(r'^[A-Z]{1}:\\$')
    else:
        sys_root = re.compile('^/$')
    curr = os.getcwd()
    while not os.path.isfile(os.path.join(curr, APP_CONFIG)):
        if sys_root.match(curr):
            return 'fail', original_dir
        os.chdir('../')
        curr = os.getcwd()
    return 'success', original_dir

def get_aos_version(root=None):
    '''Figure out the version of AliOS-Things'''
    ver = ''
    orig_dir = None

    if not root:
        ret, orig_dir = cd_aos_root()
        if ret == "fail":
            return None
        else:
            root = os.getcwd()

    ver_file = os.path.join(root, "include", "aos", "kernel.h")
    if os.path.isfile(ver_file):
        with open(ver_file, 'r') as f:
            l = f.readline()
            while l:
                verlist = re.findall(r'.*#define SYSINFO_KERNEL_VERSION\s+\"AOS-R-([0-9|\.]+)\".*', l)
                if verlist:
                    ver = verlist[0]
                    break
                l = f.readline()

    if orig_dir and os.path.isdir(orig_dir):
        os.chdir(orig_dir)

    return ver

def get_aos_project():
    """ Figure out the aos project dir """
    curr_dir = os.getcwd()

    host_os = get_host_os()
    if host_os == 'Win32':
        sys_root = re.compile(r'^[A-Z]{1}:\\$')
    else:
        sys_root = re.compile('^/$')

    while not os.path.isfile(os.path.join(curr_dir, ".aos", OS_CONFIG)):
        curr_dir = os.path.abspath(os.path.join(curr_dir, "../"))

        if sys_root.match(curr_dir):
            return None

    return curr_dir

def which(program, extra_path=None):
    if platform.system() == 'Windows' and program.endswith('.exe') == False:
        program += '.exe'

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        paths = os.environ["PATH"].split(os.pathsep)
        if extra_path:
            paths += extra_path.split(os.pathsep)

        for path in paths:
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

def cmd_version_match(cmd, version):
    cmd = which(cmd)
    if cmd == None:
        return False
    if version == 'all':
        return True
    match = False
    try:
        ret = subprocess.check_output([cmd, '-v'], stderr=subprocess.STDOUT)
    except:
        return match
    lines = ret.decode().split('\n')
    for line in lines:
        if version in line:
            match = True
            break;
    return match

def get_config_value(keyword, config_file=None):
    """ Get value of keyword from config file """
    value = None
    if not config_file:
        config_file = '.config'

    if not os.path.isfile(config_file):
        return value

    with open(config_file) as f:
        for line in f.readlines():
            match = re.match(r'^([\w+-]+)\=(.*)$', line)
            if match and match.group(1) == keyword:
                value = match.group(2).replace('"','')

    return value

def get_board_dir(board, source_root, board_dirs=None):
    """ Get board dir that include version number """
    board_dir = None
    subdirs = ["board", "kernel/board", "platform/board", "vendor/board"]
    if board_dirs:
        subdirs += board_dirs

    for subdir in subdirs:
        tmp = os.path.join(source_root, subdir, board)
        if os.path.isdir(tmp):
            board_dir = tmp
            break
    if not board_dir and board == "board_comp_make":
        board_dir = board
    return board_dir

def update_config_in():
    """ Call build/scripts/gen_configin.py """
    ret = 0
    gen_config_script = "build/scripts/gen_configin.py"
    if os.path.isfile(gen_config_script):
        ret = popen(gen_config_script)

    return ret

def check_url(url):
    """ Check if the url available """
    ret = 0
    code = 404

    try:
        from urllib2 import urlopen
    except:
        from urllib.request import urlopen

    try:
        resp = urlopen(url)
        code = resp.getcode()
    except:
        pass

    if code != 200:
        ret = 1

    return ret

def get_locale():
    try:
        enc = locale.getdefaultlocale()
    except Exception as e:
        if not os.environ.get("LC_ALL"):
            os.environ['LC_ALL'] = "en_US.UTF-8"
            os.environ['LANG'] = "en_US.UTF-8"
            enc = locale.getdefaultlocale()
        else:
            error("Failed to get locale, error: %s" % format(e))

    if not enc or not enc[1]:
        return 'utf-8'
    else:
        return enc[1]

def locale_to_unicode(str):
    if str and sys.version_info[0] == 2 and not isinstance(str, unicode):
        return unicode(str, get_locale())
    else:
        return str

class Config():
    def __init__(self, conf_file):
        self.conf = conf_file

    def get(self, keyword):
        value = None
        with open(self.conf, "r") as f:
            for line in f.readlines():
                m = re.match(r'^([\w+-]+)\=(.*)$', line)
                if m and m.group(1) == keyword:
                    value = m.group(2)

        return value
