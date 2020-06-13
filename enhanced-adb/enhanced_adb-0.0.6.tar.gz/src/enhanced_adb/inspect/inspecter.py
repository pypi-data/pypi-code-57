import logging
import os
import re
import sys

from ..inspect import permission_data, str_res_table

from .inspect_result import InspectResult
from .manifest_parser import Manifest


'''
regular express

'''
re_packageName = re.compile(r"package: name=\'([^\']+)\'")
re_versionCode = re.compile(r"versionCode=\'([^\']+)\'")
re_versionName = re.compile(r"versionName=\'([^\']+)\'")

re_compileSdkVersion = re.compile(r"compileSdkVersion=\'([^\']+)\'")
re_sdkVersion = re.compile(r"sdkVersion:\'([^\']+)\'")
re_targetSdkVersion = re.compile(r"targetSdkVersion:\'([^\']+)\'")

re_permission_group = re.compile(r"uses-permission:\s([^\n]+)")
re_permission_name = re.compile(r"name=\'([^\']+)\'")

re_label = re.compile(r"application: label=\'([^\']+)\'")


class Permission:
    def __init__(self, name):
        self._name = name

        item = permission_data.get(name)

        if item:
            self._level = item.get('level')
            self._description = item.get('description')
        else:
            self._level = 'Unknown'
            self._description = 'Unknown'

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @level.getter
    def level(self):
        return str(self._level)

    @property
    def description(self):
        return self._description


def _check_path_and_format(path):
    if os.path.isabs(path):
        apk_path = path
    else:
        apk_path = os.path.abspath(path)

    if not os.path.exists(apk_path):
        logging.error("file \"{0}\" not found".format(apk_path))
        return None

    return apk_path


def _get_re_group_result(re_exp, text):
    try:
        g = re_exp.search(text).groups()
        if not g or len(g) == 0:
            print("can't found {}".format(re_exp), file=sys.stderr)
            raise RuntimeError

        return g[0]
    except AttributeError:
        return None


def do_inspect(arg_path):
    logging.debug("inspect [{}]...".format(arg_path))
    # check path
    logging.debug("check path")
    abs_path = _check_path_and_format(arg_path)
    if not abs_path:
        return None

    result: InspectResult = InspectResult(abs_path)

    import zipfile
    from zipfile import BadZipFile

    apk = None
    try:
        apk = zipfile.ZipFile(abs_path, 'r')
    except BadZipFile:
        logging.error("File is not a apk or zip file")

    if not apk:
        return None

    cert = apk.open("META-INF/CERT.RSA")

    from ..aapt.aapt import AAPT

    from io import StringIO
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    log = logging.getLogger('root')
    log.addHandler(handler)

    cmd = AAPT.cmd(["dump", "badging", abs_path])

    err = cmd.stderr

    if err:
        logging.error(err.decode("utf-8"))
        return None

    badging_result = cmd.stdout.decode("utf-8")

    label_str = _get_re_group_result(re_label, badging_result)
    logging.debug("label: {}".format(label_str))
    result.label = label_str

    packageName_str = _get_re_group_result(re_packageName, badging_result)
    logging.debug("package_name: {}".format(packageName_str))
    result.package = packageName_str

    versionName_str = _get_re_group_result(re_versionName, badging_result)
    logging.debug("version_name: {}".format(versionName_str))
    result.version = versionName_str

    versionCode_str = _get_re_group_result(re_versionCode, badging_result)
    logging.debug("version_code: {}".format(versionCode_str))
    result.version_code = versionCode_str

    compileSdkVersion_str = _get_re_group_result(re_compileSdkVersion, badging_result)
    targetSdkVersion_str = _get_re_group_result(re_targetSdkVersion, badging_result)
    sdkVersion_str = _get_re_group_result(re_sdkVersion, badging_result)
    result.set_compile_setting(compileSdkVersion_str, sdkVersion_str, targetSdkVersion_str)

    permissions_result = re_permission_group.findall(badging_result)

    for perm in permissions_result:
        name_str = _get_re_group_result(re_permission_name, perm)
        result.add_permission(Permission(name_str))

    manifest_result = AAPT.cmd(["dump", "--values", "xmltree", abs_path, "AndroidManifest.xml"])

    # res_string = AAPT.cmd(["dump", "--values", "resources", abs_path])
    # print(res_string.stdout.decode("utf-8"))

    if not manifest_result.stderr:
        manifest = Manifest(manifest_result.stdout.decode("utf-8"))
        result.manifest = manifest

    files = apk.filelist
    for file in files:
        if file.filename.endswith('.properties'):
            text = apk.open(file, "r").read().decode("utf-8")
            result.add_properties(file.filename, text)



    return result
