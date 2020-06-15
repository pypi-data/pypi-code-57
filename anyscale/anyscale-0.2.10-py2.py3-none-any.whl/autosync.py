import copy
import os
import subprocess
import sys
import xml.etree.ElementTree


class AutosyncRunner:
    def __init__(self) -> None:
        self.syncthing_home = os.path.expanduser("~/.anyscale/syncthing")
        self.syncthing_config_path = os.path.join(self.syncthing_home, "config.xml")
        # Make it so syncthing does not try to automatically update itself.
        # This also avoids configurations getting out of sync.
        # We should only roll out new versions deliberately after testing.
        self.env = os.environ.copy()
        self.env["STNOUPGRADE"] = "1"

        # Get the right syncthing executable path depending on the OS.
        current_dir = os.path.dirname(os.path.realpath(__file__))
        if sys.platform.startswith("linux"):
            self.syncthing_executable = os.path.join(current_dir, "syncthing-linux")
        elif sys.platform.startswith("darwin"):
            self.syncthing_executable = os.path.join(current_dir, "syncthing-macos")
        else:
            raise NotImplementedError(
                "Autosync not supported on platform {}".format(sys.platform)
            )

        # This line creates the configuration file for the autosync.
        assert (
            subprocess.check_call(
                [
                    self.syncthing_executable,
                    "-allow-newer-config",
                    "-generate",
                    self.syncthing_home,
                ],
                env=self.env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            == 0
        )

        # Deactivate the user reporting.
        config = xml.etree.ElementTree.parse(self.syncthing_config_path)
        root = config.getroot()
        for child in root.getchildren():
            if child.tag == "options":
                for element in child.getchildren():
                    if element.tag == "urAccepted":
                        element.text = "-1"
        config.write(self.syncthing_config_path)

    def add_device(self, project_name: str, device_id: str) -> None:
        """Add a device to syncthing config to device and folder section.

        The syncthing configuration path used is in the SYNCTHING_CONFIG_PATH
        variable. If this device_id has already been added it will not be
        added again.

        Args:
            project_name: Name of the project we add the device to.
            device_id: ID of the device being added.
        """
        config = xml.etree.ElementTree.parse(self.syncthing_config_path)
        root = config.getroot()
        project_folder_element = None
        device_element = None
        for child in root.getchildren():
            if child.get("id") == project_name:
                project_folder_element = child
            if child.get("id") == device_id:
                device_element = child
        assert project_folder_element is not None
        # Add the device element to the top level configuration if it
        # is not already there.
        if not device_element:
            device_element = xml.etree.ElementTree.SubElement(
                root,
                "device",
                {
                    "compression": "metadata",
                    "id": device_id,
                    "introducedBy": "",
                    "introducer": "false",
                    "name": project_name,
                    "skipIntroductionRemovals": "false",
                },
            )
            properties = {
                "address": "dynamic",
                "paused": "false",
                "autoAcceptFolders": "false",
                "maxSendKbps": "0",
                "maxRecvKbps": "0",
                "maxRequestKiB": "0",
            }
            for key, value in properties.items():
                element = xml.etree.ElementTree.SubElement(device_element, key)
                element.text = value
            root.append(device_element)

        # We want to add the device element to the folder if it is
        # not already there. First check if it is, then add it if needed.
        folder_device_element_present = False
        for child in project_folder_element.getchildren():
            if project_folder_element.get("id") == device_id:
                folder_device_element_present = True
        if not folder_device_element_present:
            folder_device_element = xml.etree.ElementTree.SubElement(
                project_folder_element, "device", {"id": device_id}
            )
            project_folder_element.append(folder_device_element)

        config.write(self.syncthing_config_path)

    def add_or_update_project_folder(
        self, project_name: str, project_folder_path: str
    ) -> None:
        """Add a project folder to the syncthing config.xml.

        The syncthing configuration path used is in the SYNCTHING_CONFIG_PATH
        variable. This function will not add any devices to the folder.

        Args:
            project_name: Name of the project we add the folder
                for. This is used as an identifier for the folder.
            project_folder_path: Full path to the folder we want
                to add to syncthing.
        """
        config = xml.etree.ElementTree.parse(self.syncthing_config_path)
        root = config.getroot()
        default_folder_element = None
        project_folder_element = None
        for child in root.getchildren():
            if child.get("id") == "default":
                default_folder_element = child
            if child.get("id") == project_name:
                project_folder_element = child
        assert default_folder_element is not None
        if not project_folder_element:
            project_folder_element = copy.deepcopy(default_folder_element)
            project_folder_element.set("id", project_name)
            project_folder_element.set(
                "label", "Project Folder for {}".format(project_name)
            )
            project_folder_element.set("path", project_folder_path)
            project_folder_element.set("fsWatcherDelayS", "1")
            root.append(project_folder_element)
        else:
            project_folder_element.set("path", project_folder_path)
        config.write(self.syncthing_config_path)

    def get_device_id(self) -> str:
        return (
            subprocess.check_output(
                [
                    self.syncthing_executable,
                    "-allow-newer-config",
                    "-home",
                    self.syncthing_home,
                    "-device-id",
                ],
                env=self.env,
            )
            .decode()
            .strip()
        )

    def start_autosync(self, verbose: bool) -> None:
        command = [
            self.syncthing_executable,
            "-allow-newer-config",
            "-home",
            self.syncthing_home,
            "-no-browser",
        ]
        if not verbose:
            syncthing = subprocess.Popen(
                command,
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            success = False
            while True:
                if syncthing.stdout:
                    line = syncthing.stdout.readline()
                    if not line:
                        break
                    if b"GUI and API listening on" in line:
                        address = line.decode().split()[-1]
                        print(
                            "Autosync is active while this program is running, "
                            "status is available at {}...".format(address)
                        )
                        success = True
                else:
                    print("Autosync is active while this program is running...")
            if not success:
                print(
                    "Autosync failed. Please retry with the --verbose flag to see the error."
                )
        else:
            syncthing = subprocess.Popen(command, env=self.env)
            syncthing.communicate()

    def kill_autosync(self) -> None:
        subprocess.check_output(["pkill syncthing || true"], shell=True)
