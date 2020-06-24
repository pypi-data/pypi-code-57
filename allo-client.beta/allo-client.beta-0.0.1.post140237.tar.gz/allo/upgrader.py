# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as Elt
from .xmlerror import ErrorCodes


class AlloUpgrader:
    repo_path = None

    def __init__(self, repo_path):
        self.repo_path = repo_path

    def verify_package_xml(self):
        """
        Verify the package.xml file with packaging.xsd schema
        """
        res = os.system("xmllint --noout --schema packaging.xsd {} 2>/dev/null".format(
            self.repo_path + '/package.xml'))
        self.handle_xmllint_result_code(os.WEXITSTATUS(res))

    @staticmethod
    def run_next_cmd_as_root():
        euid = os.geteuid()
        if euid != 0:
            print("Script not started as root. Running sudo..")
            # the next line replaces the currently-running process with the sudo
            os.system('sudo' + ' echo "Logged in as root"')

    @staticmethod
    def handle_xmllint_result_code(code: int):
        default = {"message": "Unknown error.",
                   "return": ErrorCodes.UNKNOWN}
        switcher = {
            0: {"pass": True},
            1: {"message": "The package description file is not a valid XML.",
                "return": ErrorCodes.INVALID_XML},
            3: {"message": "The package description file is not valid.",
                "return": ErrorCodes.INVALID_WITH_XSD},
            127: {"messsage": "The command xmllint is not installed. Please install it and retry.",
                  "return": ErrorCodes.XMLLINT_NOT_FOUND}
        }
        handler = switcher.get(code, default)
        if not handler.get("pass"):
            print(handler.get("message"))
            exit(handler.get("return"))

    def get_root_element(self) -> Elt.Element:
        with open(self.repo_path + '/package.xml', "rb") as file:
            test = Elt.parse(file)
        return test.getroot()

    def do_upgrade(self, version):
        _rootel = self.get_root_element()

        upgrade_el = _rootel.find("Upgrades").findall("Upgrade[@Version='{}']".format(version))

        for to_upgrade in upgrade_el:
            scripts = to_upgrade.findall("Script")
            if len(scripts) > 0:
                for sh in scripts:
                    executable = "ansible-playbook --extra-vars \"repo_path={}\" ".format(self.repo_path) + \
                                 os.path.join(self.repo_path, sh.get("File"))
                    if sh.get("Sudo"):
                        self.run_next_cmd_as_root()
                        executable = "sudo " + executable
                    oscall_result = os.system(executable)
                    if os.WEXITSTATUS(oscall_result) != 0:
                        print("Error on upgrade script {}".format(sh.get("File")))
                        return os.WEXITSTATUS(oscall_result)

        print("Upgrading to version {} complete with success".format(version))
        return 0

    def do_install(self):
        executable = "ansible-playbook --extra-vars \"repo_path={}\" ".format(self.repo_path) + \
                     os.path.join(self.repo_path, "scripts/install.yml")
        self.run_next_cmd_as_root()
        executable = "sudo " + executable
        oscall_result = os.system(executable)
        if os.WEXITSTATUS(oscall_result) != 0:
            print("Error on install script")
            return os.WEXITSTATUS(oscall_result)
