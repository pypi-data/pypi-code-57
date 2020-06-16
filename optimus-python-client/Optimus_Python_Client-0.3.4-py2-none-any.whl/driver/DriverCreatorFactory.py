from driver.AndroidDriverFactory import AndroidDriverCreator
from driver.IosDriverFactory import IosDriverCreator


class DriverCreatorFactory(object):

    @classmethod
    def getInstance(cls, sessionUrl, desiredCapabilities):
        if desiredCapabilities.get("platformName").__str__().lower() == "android":
            return AndroidDriverCreator().getDriver(sessionUrl, desiredCapabilities)
        elif desiredCapabilities.get("platformName").__str__().lower() == "ios":
            return IosDriverCreator().getDriver(sessionUrl, desiredCapabilities)
        else:
            raise Exception("Cannot find platformName capability to create a new driver")
