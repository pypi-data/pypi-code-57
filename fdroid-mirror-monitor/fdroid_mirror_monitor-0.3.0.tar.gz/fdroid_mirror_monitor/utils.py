#!/usr/bin/env python3

# stdlibs:
from datetime import datetime, timezone
from urllib.parse import urlparse
import logging
import os
import re
import requests
import shutil
import subprocess
import tempfile

# external:
from PIL import Image
import coloredlogs
import GeoIP
import pyqrcode

log_level = None


def get_logger(name=__name__, verbosity=None):
    '''
    Colored logging

    :param name: logger name (use __name__ variable)
    :param verbosity:
    :return: Logger
    '''
    global log_level
    if verbosity is not None:
        if log_level is None:
            log_level = verbosity
        else:
            raise RuntimeError('Verbosity has already been set.')

    shortname = name.replace('fdroid_mirror_monitor.', '')
    logger = logging.getLogger(shortname)

    # no logging of libs (and fix double logs because of fdroidserver)
    logger.propagate = False

    fmt = '%(asctime)s %(threadName)-34s %(name)-7s %(levelname)-8s %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S%z'

    fs = {
        'asctime': {'color': 'green'},
        'hostname': {'color': 'magenta'},
        'levelname': {'color': 'red', 'bold': True},
        'name': {'color': 'magenta'},
        'programname': {'color': 'cyan'},
        'username': {'color': 'yellow'},
    }

    ls = {
        'critical': {'color': 'red', 'bold': True},
        'debug': {'color': 'green'},
        'error': {'color': 'red'},
        'info': {},
        'notice': {'color': 'magenta'},
        'spam': {'color': 'green', 'faint': True},
        'success': {'color': 'green', 'bold': True},
        'verbose': {'color': 'blue'},
        'warning': {'color': 'yellow'},
    }

    coloredlogs.install(level=log_level, logger=logger, fmt=fmt, datefmt=datefmt, level_styles=ls, field_styles=fs)

    return logger


def get_mirrors_readme(filepath='README.md', archivecheck=False):
    '''
    Extract mirror URLs of https://f-droid.org repos from README.md

    :param filepath: path to README.md\n
    :param archivecheck: check if mirror hosts archive repo\n
    :return: repo mirrors, archive mirrors
    '''
    from fdroid_mirror_monitor.mirror import Mirror

    with open(filepath) as fp:
        readme = fp.read()

    teststr = '## Active Mirrors of https://f-droid.org'
    repo_only_teststr = '### repo only'
    archive = True

    repo_mirrors = []
    archive_mirrors = []

    start_idx = readme.find(teststr) + len(teststr) + 1
    for line in readme[start_idx:].split('\n'):
        if line.strip() == repo_only_teststr:
            archive = False

        match = re.match('^\\s*\\*\\s*(http\\S*|rsync\\S*)(\\s+?RSYNC_PASSWORD=(.*))?', line)
        if match is None:
            continue

        url = match.group(1)
        rsync_pw = match.group(3)

        # recheck if mirror still mirrors archive repo or if mirror now mirrors archive
        if archivecheck is True:
            has_archive_readme = archive
            archive = Generic(rsync_pw=rsync_pw).check_file(url + 'archive/index-v1.jar')
            if has_archive_readme != archive:
                log = get_logger(__name__)
                if has_archive_readme is True:
                    log.warning('Please update README.md. Mirror %s does not mirror archive!')
                else:
                    log.warning('Please update README.md. Mirror %s mirrors archive!')

        m = Mirror(url + 'repo/', rsync_pw=rsync_pw)
        repo_mirrors.append(m)

        if archive is True:
            m = Mirror(url + 'archive/', rsync_pw=rsync_pw)
            archive_mirrors.append(m)

    return repo_mirrors, archive_mirrors


def geoip(ip):
    '''
    :param ip: IPv4 or IPv4 address
    :return: tuple of country_name and country_code
    '''
    if ':' in ip:
        # IPv6
        gi6 = GeoIP.open("/usr/share/GeoIP/GeoIPv6.dat", GeoIP.GEOIP_STANDARD)

        return gi6.country_name_by_addr_v6(ip), gi6.country_code_by_addr_v6(ip)

    else:
        # IPv4
        gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

        return gi.country_name_by_addr(ip), gi.country_code_by_addr(ip)


def get_own_ip(timeout=60):
    r = requests.get('https://ident.me')

    try:
        r.raise_for_status()
    except Exception as e:
        log = get_logger(__name__)
        log.warning(str(e))
        log.error('Failed to get own ip from ident.me')
        return None

    return r.text


def get_repos_izzy(timeout=60):
    '''
    Extract repos from 'https://android.izzysoft.de/articles/named/list-of-fdroid-repos'

    :return: array of repo urls
    '''
    log = get_logger(__name__)
    izzy_url = 'https://android.izzysoft.de/articles/named/list-of-fdroid-repos'

    r = requests.get(izzy_url, allow_redirects=True, timeout=timeout)
    try:
        r.raise_for_status()
    except Exception as e:
        log.error('Could not collect from izzy: %s' % str(e))
        return []

    repos = []
    for line in re.findall('<td align="center">.*', r.text):
        print('ll', line)
        repos.extend(re.findall('http[^<]+', line))

    return sorted(repos)


def get_repos_wiki(timeout=60):
    '''
    Extract repos from 'https://forum.f-droid.org/t/known-repositories/721.json'
    :return: array of repo urls
    '''
    log = get_logger(__name__)
    wikiurl = 'https://forum.f-droid.org/t/known-repositories/721.json'

    r = requests.get(wikiurl, allow_redirects=True, timeout=timeout)
    try:
        r.raise_for_status()
    except Exception as e:
        log.error('Could not get repos from wiki: %s' % str(e))
        return []

    data = r.json()

    links = set()
    repos = set()
    for link in data['details']['links']:
        links.add(link['url'])
    for link in links:
        if urlparse(link).query.startswith('fingerprint='):
            repos.add(link)

    return sorted(repos)


def qr(data, out_path, logo_path='fdroid-logo_300.png'):
    '''
    :param data: url or orther data
    :param path: filepath to save the QRCode png
    '''
    # Generate the qr code and save as png
    qr = pyqrcode.QRCode(data)
    qr.png('/tmp/qr_tmp.png', scale=5, quiet_zone=2)

    # Now open that png image to put the logo
    img = Image.open('/tmp/qr_tmp.png')
    img = img.convert('RGBA')
    width, height = img.size

    # How big the logo we want to put in the qr code png
    logo_size = width / 3

    # Calculate xmin, ymin, xmax, ymax to put the logo
    xmin = ymin = int((width / 2) - (logo_size / 2))
    xmax = ymax = int((width / 2) + (logo_size / 2))

    # Open the logo image
    logo = Image.open(logo_path)

    # resize the logo as calculated
    logo = logo.resize((xmax - xmin, ymax - ymin))

    # put the logo in the qr code
    img.convert("RGBA")
    img.paste(logo, (xmin, ymin, xmax, ymax), logo)

    with open(out_path, 'wb') as fp:
        img.save(fp)


class Generic:
    def __init__(
        self,
        url=None,
        rsync_pw=None,
        timeout=60,
        headers={'User-Agent': 'https://gitlab.com/marzzzello/mirror-monitor'},
    ):
        self.url = url
        self.rsync_pw = rsync_pw
        self.timeout = timeout
        self.headers = headers

    def init_protocols(self):
        '''
        - needs self.url to be set
        - set self.protocol to http(s), rsync
        - set self.hostname, self.path and self.onion
        - add trailing slash for self.url
        '''
        # add trailing slash
        if self.url.endswith('/') is False:
            self.url += '/'
        u = urlparse(self.url)
        self.hostname = u.hostname
        self.path = u.path
        if u.scheme == 'https' or u.scheme == 'http' or u.scheme == 'rsync':
            self.protocol = u.scheme
        else:
            self.protocol = 'unknown'

        if self.hostname.endswith('.onion'):
            self.onion = True
        else:
            self.onion = False

    def get_file(self, url):
        '''
        Download file from url
        needs self.headers and self.timeout to be set
        :return: filepointer, modified datetime, size in bytes, headers dict
        '''
        if urlparse(url).hostname.endswith('.onion'):
            raise ValueError('''Getting file via Tor is not supported (yet) %s''' % url)

        if url.startswith('http://') or url.startswith('https://'):
            return self._get_http_s(url)
        elif url.startswith('rsync://'):
            return self._get_rsync(url)
        else:
            raise ValueError('''Can't get file with unknown protocol %s''' % url)

    def _get_http_s(self, url, delete=False):
        with requests.get(url, stream=True, headers=self.headers, timeout=self.timeout) as r:
            r.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=delete) as fp:
                shutil.copyfileobj(r.raw, fp)

                t_fmt = r.headers['last-modified']
                dt = datetime.strptime(t_fmt, '%a, %d %b %Y %H:%M:%S GMT')
                dt = dt.replace(tzinfo=timezone.utc)

                return fp, dt, r.headers['content-length'], dict(r.headers)

    def _get_rsync(self, url, delete=False):
        if self.rsync_pw is None:
            env = None
        else:
            env = {'RSYNC_PASSWORD': self.rsync_pw}

        rsync_cmd = ['rsync', '--quiet', '-ax', '--contimeout=%d' % self.timeout, '--timeout=%d' % self.timeout]
        rsync_cmd.append(url)

        with tempfile.NamedTemporaryFile(delete=delete) as fp:
            rsync_cmd.append(fp.name)
            p = subprocess.run(rsync_cmd, capture_output=True, text=True, env=env)
        if p.returncode == 0:
            s = os.stat(fp.name)
            dt = datetime.fromtimestamp(s.st_mtime, timezone.utc)
            dt = dt.replace(microsecond=0)

            return fp, dt, s.st_size, None
        else:
            raise subprocess.CalledProcessError(
                cmd=rsync_cmd, returncode=p.returncode, stderr=p.stderr, output=p.stdout
            )

    def check_file(self, url):
        '''
        Check file from url

        needs self.headers and self.timeout to be set

        :return: True if file exists, False if not
        '''
        if urlparse(url).hostname.endswith('.onion'):
            raise ValueError('''Getting file via Tor is not supported (yet) %s''' % url)

        if url.startswith('http://') or url.startswith('https://'):
            return self._check_file_http_s(url)
        elif url.startswith('rsync://'):
            return self._check_file_rsync(url)
        else:
            raise ValueError('''Can't get file with unknown protocol %s''' % url)

    def _check_file_http_s(self, url):
        r = requests.head(url, timeout=self.timeout, headers=self.headers)
        if r.status_code == 200:
            return True
        elif r.status_code == 404:
            return False
        else:
            r.raise_for_status()

    def _check_file_rsync(self, url):
        if self.rsync_pw is None:
            env = None
        else:
            env = {'RSYNC_PASSWORD': self.rsync_pw}

        rsync_cmd = ['rsync', '--quiet', '--list-only', '--contimeout=%d' % self.timeout, '--timeout=%d' % self.timeout]
        rsync_cmd.append(url)
        p = subprocess.run(rsync_cmd, capture_output=True, text=True, env=env)

        if p.returncode == 0:
            return True
        elif p.returncode == 23:
            return False
        else:
            raise subprocess.CalledProcessError(
                cmd=rsync_cmd, returncode=p.returncode, stderr=p.stderr, output=p.stdout
            )
