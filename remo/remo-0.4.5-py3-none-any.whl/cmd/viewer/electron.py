import os
import re
import platform
import subprocess
from pathlib import Path

linux_path = 'app/remo'
darwin_path = 'app/remo.app/Contents/MacOS/remo'
windows_path = 'app/remo.exe'
REMO_HOME = os.getenv('REMO_HOME', str(Path.home().joinpath('.remo')))
url_rxp = re.compile(r'(http[s]?://[.\w-]+)(:([0-9]+))?/?([\/\w-]+)?')


def browse(url, debug=False):
    host, port, page = split_ulr(url)
    remo = get_executable_path()
    kwargs = {
        'host': host,
        'port': port,
        'page': page
    }
    if debug:
        kwargs['debug'] = 'true'

    cmd = build_cmd(remo, **kwargs)
    subprocess.Popen(cmd, shell=True)


def split_ulr(url):
    host, _, port, page = url_rxp.match(url).groups()
    return host, port, page


def build_cmd(executable, **kwargs):
    cmd = '{} {}'.format(executable, ' '.join('--{}={}'.format(k, v) for k, v in kwargs.items() if v))
    return cmd


def get_executable_path():
    name = platform.system()
    if name == 'Windows':
        exe_path = windows_path
    elif name == 'Darwin':
        exe_path = darwin_path
    elif name == 'Linux':
        exe_path = linux_path
    return str(os.path.join(REMO_HOME, exe_path))
