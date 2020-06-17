import os
import re
from aos.managers.constant import *
from aos.managers.misc import aos_warning, aos_error
from aos.util import debug

if PYURLPKG == 'urlgrabber':
    from urlgrabber.grabber import URLGrabber
    from urlgrabber.grabber import URLGrabError
elif PYURLPKG == 'requests':
    import requests

''' related definitions
## general
PKG_QUERY_URL = "http://xxx/cube/getComponentVersionOfSystemVersion"
PKG_QUERY_HTTP_HEADER = "Content-Type:application/json"
PKG_QUERY_HTTP_METHOD = "POST"
## ver query
PKG_VER_QUERY_API = "/getComponentVersionOfSystemVersion"
PKG_VER_QUERY_DATA_FORMAT = "{\"compName\": \"%s\", \"systemVersion\":\"%s\"}"
'''

class QueryServer():
    def __init__(self, url=None):
        if url:
            self.url = url
        else:
            self.url = PKG_QUERY_URL

        self.hdr = PKG_QUERY_HTTP_HEADER
        self.method = PKG_QUERY_HTTP_METHOD

        self.ver_api = PKG_VER_QUERY_API
        self.dep_api = PKG_DEP_QUERY_API
        self.clist_api = PKG_CLIST_QUERY_API
        self.ver_data_fmt = PKG_VER_QUERY_DATA_FORMAT
        self.dep_data_fmt = PKG_DEP_QUERY_DATA_FORMAT
        self.clist_data_fmt = PKG_CLIST_QUERY_DATA_FORMAT

    def _query_helper(self, api, d):
        result = None
        hdrname = re.findall(r'(.+):.+', self.hdr)
        hdrvalue = re.findall(r'.+:(.+)', self.hdr)
 
        if not hdrname or not hdrvalue:
            aos_warning("invalid http header provided: %s" % hdr)
            return None

        if PYURLPKG == 'urlgrabber':
            ug = URLGrabber(reget='simple', http_headers=((hdrname[0], hdrvalue[0]),))

            try:
                debug("url: %s, data: %s" % (self.url + api, d))
                f = ug.urlopen(self.url + api, data=d)
                result = f.read()
            except URLGrabError as e:
                aos_warning("Failed to connect the query server (error: %s)!" % format(e))
        elif PYURLPKG == 'requests':
            try:
                http_header={hdrname[0]:hdrvalue[0]}
                r = requests.post(self.url + api, headers=http_header, data=d)
                if r.status_code == 200:
                    result = r.content
            except Exception as e:
                aos_warning("Failed to do http POST request for %s: %s" % (self.url + api, format(e)))
        else:
            aos_error("The url package %s is not supported!" % PYURLPKG)

        return result

    '''
    - Server flow:
    ## API: /getComponentVersionOfSystemVersion
    ## request
    { 
      "compName": "mcu_moc108", 
      "systemVersion":"3.0.0"
    }
    ## response
    { 
      "success":true/false,
      "message":"success/xxx error",
      "result":["1.0.1.2","2.0.0"]
    }

    - This API returns a list of version numbers.
    '''
    def query_ver(self, pkgname, osver):
        data = self.ver_data_fmt % (pkgname, osver)
        #data = "{\"compName\": \"%s\", \"systemVersion\":\"%s\"}" % ("yloop", "3.0.0")
        v = self._query_helper(self.ver_api, data)

        if v:
            vstr = bytes.decode(v)

        if not v or not vstr.startswith("{\"success\":true"):
            aos_warning("Failed to query version information")
            return []

        #vstr = re.findall(r'.+,\"result\":\"\[(.+)\]\"}', v)
        vstr = re.findall(r'.+,\"result\":\[(.+)\]}', vstr)

        if vstr and vstr[0] != 'null':
            return list((lambda x:x.strip("\""))(x) for x in vstr[0].split(','))
        else:
            return []

    '''
    - Server flow:
    ## API: /getComponentDependency
    ## request
    { 
      "name":"board_asr5501", 
      "version":"1.0.0"
    }
    ## response
    {
      "success":true/false,
      "message":"success/xxx error",
      "result":"[{'max_version':'','min_version':'1.0.0','name':'netmgr'},{'max_version':'','min_version':'1.0.0','name':'mcu_asr5501'},{'max_version':'','min_version':'1.0.0','name':'kernel_init'}]"
    }

     - This API returns a list of dict of pkg info: [{"min":"1.0.0","max":"3.0.0","name":"netmgr"}, {}, {}]
    '''
    def query_dep(self, pkgname, pkgver):
        data = self.dep_data_fmt % (pkgname, pkgver)
        d = self._query_helper(self.dep_api, data)

        if d:
            dstr = bytes.decode(d)

        if not d or not dstr.startswith('{"success":true'):
            aos_warning("Failed to query version information")
            return []

        dstr = re.findall(r'.+,\"result\":\"\[(.+)\]\"}', dstr)

        if dstr:
            dlist = dstr[0].split('},{')
        else:
            return []

        ret_list = []
        for d in dlist:
            max = re.findall(r'.*max_version[\'\"]:[\'\"]([0-9|\.]*)[\'|\"].*', d)
            min = re.findall(r'.*min_version[\'\"]:[\'\"]([0-9|\.]*)[\'|\"].*', d)
            name = re.findall(r'.*name[\'\"]:[\'\"]([a-zA-Z0-9]+)[\'|\"].*', d)

            if not max[0]:
                max[0] = '0.0.0'

            if not min[0]:
                min[0] = '0.0.0'

            if name:
                ret_list.append(dict(zip([DEP_NAME, DEP_VER_MIN, DEP_VER_MAX],
                                [name[0], min[0], max[0]])))

        return ret_list

    '''
    - Server flow:
    ## API: /getComponentListOfSystemVersion
    ## request
    { 
      "systemVersion":"3.0.0"
    }
    ## response
    {
      "success":true/false,
      "message":"success/xxx error",
      "componentList":[
          {"name": "rhino", "versionList": ["1.0.1"]},
          {"name": "linkkit", "versionList": ["1.0.0", "2.0.0"]}
      ]
    }

    - This API returns a list of dict of pkg name/ver information
    '''
    def query_pkginfo(self, osver, names):
        data = self.clist_data_fmt % (osver)
        p = self._query_helper(self.clist_api, data)

        if p:
            pstr = bytes.decode(p)

        if not p or not pstr.startswith('{"success":true'):
            aos_warning("Failed to query pkg list information for OS %s" % osver)
            return []

        # for test use
        #pstr = '{"success":true/false,"message":"success/xxx error","componentList":[{"name": "rhino", "versionList": ["1.0.1"]},{"name": "linkkit", "versionList": ["1.0.0", "2.0.0"]}]}'

        pstr = re.findall(r'.+,\"componentList\":\[(.+)\]}', pstr)

        if pstr:
            plist = pstr[0].split('},{')
        else:
            return []

        ret_list = []
        for p in plist:
            name = re.findall(r'.*name[\'\"]:\s*[\'"]([^\'"]+)[\'"].*', p)
            # find out "1.1.1", "2.2.2", ...
            #vers = re.findall(r'.*versionList[\'\"]:\s*\[([0-9\.\'\",\s]+)\]}', p)
            vers = re.findall(r'.*versionList[\'\"]:\s*\[([0-9\.\'",\s]+)\].*', p)

            if not name:
                continue
            else:
                name = name[0]
                # if names provided, only add the matched
                if names and name not in names:
                    continue

            if vers:
                for v in re.split(r', ', vers[0]):
                    ver = v.strip("\"")
                    if ver:
                        ret_list.append(dict(zip([pkg_name_in_dict, pkg_version_in_dict], [name, ver])))

        # Sort by name
        k = lambda s:s[pkg_name_in_dict]
        ret_list.sort(key=k)

        return ret_list
