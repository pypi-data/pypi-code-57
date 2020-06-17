#!/usr/bin/env python3

# internal:
from fdroid_mirror_monitor.utils import get_logger, Generic

# stdlibs
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit
import json
import os
import re
import socket
import ssl
import subprocess

# external:
import dns.resolver
import GeoIP
import yaml


class Mirror(Generic):
    '''
    Mirror
    '''

    instances = []
    log = get_logger(__name__)

    def __new__(
        cls,
        url,
        index_file='index-v1.jar',
        rsync_pw=None,
        timeout=60,
        headers={'User-Agent': 'https://gitlab.com/marzzzello/mirror-monitor'},
    ):
        cls.url = url
        cls.init_protocols(cls)
        cls.name = cls.protocol + ':' + cls.hostname

        existing_mirrors = cls.instances
        for mirror in existing_mirrors:
            if mirror.name == cls.name:
                cls.log.info('Mirror %s already exists. Using existing instead of creating new' % mirror.name)

                mirror.index_urls.append(url + index_file)

                if rsync_pw != mirror.rsync_pw:
                    cls.log.warning(
                        'rsync_pw differs. Prefer existing (%s) over new (%s)' % (mirror.rsync_pw, rsync_pw)
                    )

                if timeout != mirror.timeout:
                    cls.log.warning('timeout differs. Prefer existing (%s) over new (%s)' % (mirror.timeout, timeout))

                if headers != mirror.headers:
                    cls.log.warning('headers differ. Prefer existing %s over new %s' % (mirror.headers, headers))

                if cls.path in mirror.repo_fullpaths:
                    cls.log.info('repo already included: %s' % cls.path)
                else:
                    mirror.add_path(cls.path)
                    cls.log.info('new repo got added: %s' % cls.path)

                return mirror

        instance = super(Mirror, cls).__new__(cls)
        cls.instances.append(instance)
        return instance

    def __init__(
        self,
        url,
        index_file='index-v1.jar',
        rsync_pw=None,
        timeout=60,
        headers={'User-Agent': 'https://gitlab.com/marzzzello/mirror-monitor'},
    ):
        '''
        If a mirror with the same hostname and protocal exists,
        then add the path to the repo list and don't create a new mirror object.

        :param url: http(s):// or rsync:// url of mirror (with /repo/ or /archive/)
        :param index_file: file that contains the index. Normally that's 'index-v1.jar' or 'index.jar' for legacy repos.
        :param rsync_pw: optional rsync password
        :param timeout: timeout for various requests
        :param headers: http headers for various requests
        '''

        # skip init if object was already initialized
        try:
            _ = self.init
        except AttributeError:
            self.init = True
        else:
            return

        self.url = url
        self.index_file = index_file
        self.index_urls = [url + index_file]

        self.rsync_pw = rsync_pw
        self.timeout = timeout
        self.headers = headers

        self.errors = {}
        self.init_protocols()
        self.name = self.protocol + ':' + self.hostname

        self.repo_fullpaths = [self.path]
        self.repo_relpaths = []

    def add_path(self, path):
        '''
        add path and calculate relative paths and set url
        '''
        self.repo_fullpaths.append(path)

        common = os.path.commonprefix(self.repo_fullpaths)
        u = list(urlsplit(self.url))
        # replace path
        u[2] = common
        self.common_url = urlunsplit(u).rstrip('/') + '/'
        self.repo_relpaths = []
        for path in self.repo_fullpaths:
            relpath = path.split(common, 1)[1]
            self.repo_relpaths.append(relpath)

    def fetch_ip_data(self):
        '''
        Get all ip addresses and corresponding countries from DNS
        DNS exceptions are handled by logging and saved to self.errors
        '''
        if self.onion is True:
            return

        gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
        gi6 = GeoIP.open('/usr/share/GeoIP/GeoIPv6.dat', GeoIP.GEOIP_STANDARD)
        countries = []
        country_codes = []
        ipv4 = []
        ipv6 = []

        try:
            ipv6 = dns.resolver.query(self.hostname, 'AAAA')
        except dns.resolver.NoAnswer:
            pass
        except Exception as e:
            self.log.warning('IPv6: %s' % str(e))
            self.errors['IPv6'] = str(e)

        try:
            ipv4 = dns.resolver.query(self.hostname, 'A')
        except dns.resolver.NoAnswer:
            pass
        except Exception as e:
            self.log.warning('IPv4: %s' % str(e))
            self.errors['IPv4'] = str(e)

        self.IPv4 = []
        for ip in ipv4:
            self.IPv4.append(ip.to_text())
            countries.append(gi.country_name_by_addr(ip.to_text()))
            country_codes.append(gi.country_code_by_addr(ip.to_text()))

        self.IPv6 = []
        for ip in ipv6:
            self.IPv6.append(ip.to_text())
            countries.append(gi6.country_name_by_addr_v6(ip.to_text()))
            country_codes.append(gi6.country_code_by_addr_v6(ip.to_text()))

        # remove duplicates
        self.countries = list(set(countries))
        self.country_codes = list(set(country_codes))

    def get_data(self):
        '''
        :return: all important info about the mirror as dict
        '''
        data = vars(self).copy()
        # filter
        data.pop('init', None)
        data.pop('path', None)
        data.pop('headers', None)
        return data

    def run_all(self):
        self.fetch_ip_data()
        self._speedtest()
        if self.protocol == 'https':
            self.log.info('tls_version')
            try:
                self._get_tls_version()
            except Exception as e:
                err = str(e)
                self.log.warning(err)
                self.errors['tls_version'] = err

            self.log.info('tlsping')
            try:
                self._get_tlsping()
            except Exception as e:
                err = str(e)
                self.log.warning(err)
                self.errors['tlsping'] = err

            self.log.info('tls_details')
            try:
                self._get_tls_details()
            except Exception as e:
                err = str(e)
                self.log.warning(err)
                self.errors['tls_details'] = err

    ###########################
    # internal helper functions
    def _speedtest(self, delete=True):
        '''
        Download file from path and measure duration
        File exceptions are handled by logging and saved to self.errors
        :param delete: if False return filepointer to downloaded file
        '''

        def _get_weight(idx_url):
            u = list(urlsplit(idx_url))
            path = u[2]
            weight = 0
            if os.path.basename(path) == 'index-v1.jar':
                weight += 1
            if path.split('/')[1] == 'repo':
                weight += 2
            if path.split('/')[1] == 'archive':
                weight -= 1
            if path.find('repo') != -1:
                weight += 1
            if path.find('archive') != -1:
                weight -= 1
            if path.find('beta') != -1:
                weight -= 1
            if path.find('nightly') != -1:
                weight -= 1
            if path.find('test') != -1:
                weight -= 1
            return weight

        self.index_urls = sorted(self.index_urls, key=_get_weight, reverse=True)
        url = self.index_urls[0]
        self.index = {}
        self.index['url'] = url
        self.log.info('Speedtest: %s' % url)

        self.success = False
        starttime = datetime.now(timezone.utc).timestamp()
        try:
            file, dt, self.index['size'], self.index['headers'] = self.get_file(url)
            self.index['modified'] = dt.strftime('%F %T %Z')
        except Exception as e:
            try:
                if e.output:
                    self.log.debug('out: %s' % e.output.rstrip('\n'))
                if e.stderr:
                    self.log.warning('err: %s' % e.stderr.rstrip('\n'))
            except AttributeError:
                pass

            self.log.warning('duration: %s' % str(e))
            self.errors['duration'] = str(e)
        else:
            self.duration = round(datetime.now(timezone.utc).timestamp() - starttime, 2)
            self.starttime = int(starttime)
            self.success = True

            if delete is True:
                os.unlink(file.name)
            else:
                return file

    def _get_tls_version(self):
        '''
        puts TLS version in self.tls_version
        '''
        context = ssl.create_default_context()
        with socket.create_connection((self.hostname, 443), timeout=self.timeout) as sock:
            with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                self.tls_version = ssock.version()

    def _get_tlsping(self):
        '''
        puts dict of TLS handshake latency details in self.tlsping
        '''
        tlsping_cmd = ['tlsping', '-json', self.hostname + ':443']
        p = subprocess.run(tlsping_cmd, capture_output=True, text=True)
        if p.returncode == 0:
            tlsping_all = json.loads(p.stdout)
            err = tlsping_all['error']
            if err != '':
                raise Exception(err)
            self.tlsping = {}
            self.tlsping['average'] = round(tlsping_all['average'], 3)
            self.tlsping['stddev'] = round(tlsping_all['stddev'], 3)
        else:
            err = re.sub('^tlsping: ', '', p.stderr).rstrip('\n')
            raise subprocess.CalledProcessError(cmd=tlsping_cmd, returncode=p.returncode, stderr=err, output=p.stdout)

    def _get_tls_details(self):
        nmap_cmd = ['nmap', '--script', 'ssl-enum-ciphers', '-p', '443', self.hostname]
        p = subprocess.run(nmap_cmd, capture_output=True, text=True)
        if p.returncode != 0:
            raise subprocess.CalledProcessError(cmd=nmap_cmd, returncode=p.returncode, stderr=p.stderr, output=p.stdout)
        else:
            accept_pat = re.compile(r'^\|')
            yaml_pat = re.compile(r'^\|[_ ]( *)(.*:)')
            convert_pat = re.compile(r'^\| ( *)([^:]+)$')
            text = ''
            syn_ack = True
            for line in p.stdout.split('\n'):
                if re.compile(r'^443/tcp filtered').match(line):
                    syn_ack = False
                    break

                if accept_pat.match(line):
                    line = yaml_pat.sub(r'\1\2', line)
                    line = convert_pat.sub(r'\1- "\2"', line)
                    text += line + '\n'
                    if line.find('|') != -1:
                        raise ValueError('%s: Found "|" in line: %s' % (nmap_cmd, line))
            data = None
            if text:
                data = yaml.safe_load(text)

            err = False
            if data:
                try:
                    self.tls_details = data['ssl-enum-ciphers']
                except KeyError:
                    err = True
            else:
                err = True

            if err is True:
                if syn_ack is False:
                    raise ValueError('No SYN ACK received %s' % nmap_cmd)
                else:
                    raise subprocess.CalledProcessError(
                        cmd=nmap_cmd, returncode=p.returncode, stderr=p.stderr, output=p.stdout
                    )
