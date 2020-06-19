import os
import sys
import importlib
import importlib.util

from . import controller
from . import interface
from . import driver


class Manager:
    def __init__(self):
        self.ctrl = controller.Controller()
        self.drivers = {"None": driver.Driver("None")}
        self.scripts = {"None": interface.Interface("None")}
        self.driver = self.drivers["None"]
        self.script = self.scripts["None"]

    def connect(self, host, psk=None):
        self.ctrl.connect(host, psk)

    def addDriver(self, driver):
        self.drivers[driver.name] = driver

    def addDriverFile(self, path):
        specname = f"manager_driver_{len(self.drivers)}"

        spec = importlib.util.spec_from_file_location(specname, path)
        driver_module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = driver_module
        spec.loader.exec_module(driver_module)

        for i, new_driver in enumerate(driver_module.drivers):
            if not new_driver.name:
                new_driver.name = f"{specname}_{i}"
            self.drivers[new_driver.name] = new_driver

    def addScript(self, path):
        specname = f"manager_script_{len(self.scripts)}"

        spec = importlib.util.spec_from_file_location(specname, path)
        script = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = script
        spec.loader.exec_module(script)

        if not script.api.name:
            script.api.name = specname

        self.scripts[script.api.name] = script.api

    def configure(self, path):
        self.addDriversFromDirectory(os.path.join(path, "drivers"))
        self.addScriptsFromDirectory(os.path.join(path, "scripts"))

    def addDriversFromDirectory(self, path):
        files = [os.path.join(path, file) for file in os.listdir(path)
                 if file.endswith(".py")]
        for file in files:
            self.addDriverFile(file)

    def addScriptsFromDirectory(self, path):
        files = [os.path.join(path, file) for file in os.listdir(path)
                 if file.endswith(".py")]
        for file in files:
            self.addScript(file)

    def chooseDriver(self, driver):
        self.driver.close()
        self.driver = driver
        self.driver.open()

    def chooseScript(self, script):
        self.script = script

    def getStatus(self):
        status = {}

        status["driver"] = self.driver.getStatus()
        status["script"] = self.script.getStatus()
        status["relay"] = self.ctrl.getStatus()

        return status

    def handle(self):
        self.script.handle(self.driver, self.ctrl)

    def run(self):
        while True:
            self.handle()
