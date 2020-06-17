import os, sys, time, re
try:
    import requests
    import platform
    #import urllib
    import requests
    import json
    import subprocess
    from uuid import getnode
    from aos.constant import AOS_SERVER_URL, AOS_HTTP_HEADER, AOS_HTTP_METHOD
    from aos.util import debug
except Exception as e:
    print("Failure when importing module in report: %s" % format(e))
    sys.exit(1)

# AOS query/report server
SERVER_URL = AOS_SERVER_URL
HTTP_HEADER = AOS_HTTP_HEADER #"Content-Type:application/json"
REPORT_API = "/reportInfo"
# uCube install report
UCUBE_INSTALL_REPORT_DATA_FMT = "\
{\
  \"macaddr\": \"%s\",\
  \"hostos\": {\
    \"name\": \"%s\",\
    \"version\": \"%s\"\
  },\
  \"ip\": \"%s\",\
  \"location\": \"%s\",\
  \"ucubever\": \"%s\",\
  \"terminal\": \"%s\",\
  \"operateType\":\"cube install\"\
}"
# uCube operation report
UCUBE_OPERATE_REPORT_DATA_FMT = "\
{\
  \"macaddr\": \"%s\",\
  \"hostos\": {\
    \"name\": \"%s\",\
    \"version\": \"%s\"\
  },\
  \"ucubever\": \"%s\",\
  \"terminal\": \"%s\",\
  \"operateType\":\"%s\",\
  \"operateContent\":\"%s\",\
  \"operateResult\":\"%s\"\
}"

def get_mac():
    mac = getnode()
    return ':'.join(("%012x" % mac)[i:i+2] for i in range(0, 12, 2))

# return timestamp in format: 'UTC+8 2020-02-11 00:00:00'
def get_timestamp():
    # timestamp, convert to '1970-01-01 00:00:00' format
    now = int(time.time())
    now_local = time.localtime(now)
    nowstr = time.strftime("%Y-%m-%d %H:%M:%S", now_local)

    # timezone, convert to 'UTC+/-xx' format
    tz = time.timezone
    tz = (0 - tz) / 3600
    tzstr = 'UTC'
    if tz >= 0:
        tzstr += '+'
    tzstr += str(tz)

    return ' '.join([tzstr, nowstr])

def get_hostos():
    name = platform.system()
    version = platform.platform()
    return name, version

# Might be very time consuming, ensure limit of using it
def get_location():
    ip = 'unknown'
    country = 'unknown'
    city = 'unknown'
    url = "https://geolocation-db.com/json"
    try:
        #response = urllib.urlopen(url)
        #data = json.loads(response.read())
        response = requests.get(url, timeout = 10)
        if response.status_code != 200:
            return ip, country, city
        data = json.loads(response.text)
        '''
        data example: {u'city': u'Shanghai', u'longitude': 121.3997, u'latitude': 31.0456, u'state': u'Shanghai', u'IPv4': u'117.143.170.234', u'country_code': u'CN', u'country_name': u'China', u'postal': None}
        '''
        if data:
            if u'IPv4' in data.keys():
                ip = data[u'IPv4']
            if u'city' in data.keys():
                city = data[u'city']
                if not city:
                    if u'state' in data.keys():
                        city = data[u'state']
            if u'country_code' in data.keys():
                country = data[u'country_code']
    except Exception as e:
        pass

    return ip, country, city

def get_ucube_ver():
    from aos.__init__ import __version__
    return __version__

def get_terminal():
    term = 'unknown'

    try:
        hostos = platform.system()

        if hostos == 'Windows':
            # Git bash
            cmd = ['which ls']
            result = 'fail'

            try:
                out, err = aos.util.exec_cmd(cmd)
                if not err and out and 'ls' in out:
                    result = 'success'
                    term = 'git bash'
            except Exception as e:
                result = 'fail'

            if result == 'success':
                return term

            # CMD or powershell
            cmd = '(dir 2>&1 *`|echo CMD);&<# rem #>echo PowerShell'
            result = 'fail'
            try:
                out, err = aos.util.exec_cmd(cmd)
                if not err and out:
                    if 'CMD' in out:
                        term = 'CMD'
                        result = 'success'
                    elif 'PowerShell' in out:
                        term = 'PowerShell'
                        result = 'success'
            except Exception as e:
                result = 'fail'

            if result == 'success':
                return term
        elif hostos == 'Linux' or hostos == 'Darwin':
            cmd = ['echo', '$0']
            result = 'fail'
            try:
                ''' seems not working
                out, err = aos.util.exec_cmd(cmd)
                if not err and out:
                    if out == 'sh' or out == '-sh':
                        term = 'sh'
                        result = 'success'
                    elif out == 'bash' or out == '-bash':
                        term = 'bash'
                        result = 'success'
                    elif out == 'csh' or out == '-csh':
                        term = 'csh'
                        result = 'success'
                    elif out == 'ksh' or out == '-ksh':
                        term = 'ksh'
                        result = 'success'
                    elif out == 'tcsh' or out == '-tcsh':
                        term = 'tcsh'
                        result = 'success'
                    elif out == 'zsh' or out == '-zsh':
                        term = 'zsh'
                        result = 'success'
                '''
                try:
                    shell_info = {'/bin/sh': 'sh',
                                  '/bin/bash': 'bash',
                                  '/bin/csh': 'csh',
                                  '/bin/ksh': 'ksh',
                                  '/bin/tcsh': 'tcsh',
                                  '/bin/zsh': 'zsh'}
                    out = subprocess.check_output(' '.join(cmd), shell=True)
                    out = out.strip()
                    if out in shell_info.keys():
                        term = shell_info[out]
                        result = 'success'
                except Exception as e:
                    result = 'fail'
            except Exception as e:
                result = 'fail'

            if result == 'success':
                return term
        else:
            pass
    except Exception:
        pass

    return term

_mac = get_mac()
_hostname, _hostver = get_hostos()
_ucubever = get_ucube_ver()
_terminal = get_terminal()

class Report():
    def __init__(self, url=None):
        if url:
            self.url = url
        else:
            self.url = SERVER_URL

        self.hdr = HTTP_HEADER

    def _report_helper(self, api, d):
        result = None
        hdrname = re.findall(r'(.+):.+', self.hdr)
        hdrvalue = re.findall(r'.+:(.+)', self.hdr)
 
        if not hdrname or not hdrvalue:
            return None

        try:
            http_header={hdrname[0]:hdrvalue[0]}
            debug("reporting:\nurl - %s, headers - %s, data - %s" %
                  (self.url + api, format(http_header), d))
            body = d.encode(encoding='utf-8')
            r = requests.post(self.url + api, headers=http_header, data=body)
            debug("reported, return code: %d, return msg: %s" % (r.status_code, r.content))
            if r.status_code == 200:
                result = r.content
        except Exception as e:
            debug("exception in _report_helper: %s" % format(e))
            pass

        return result

    def report_install(self):
        _ip, _country, _city = get_location()
        api = REPORT_API
        data = UCUBE_INSTALL_REPORT_DATA_FMT % (_mac, _hostname,
                                                _hostver, _ip,
                                                '-'.join([_country, _city]),
                                                _ucubever, _terminal)
        return self._report_helper(api, data)

    def report_operate(self, optype, op, opresult):
        api = REPORT_API
        data = UCUBE_OPERATE_REPORT_DATA_FMT % (_mac, _hostname,
                                                _hostver, _ucubever, _terminal,
                                                optype, op, opresult)
        return self._report_helper(api, data)
