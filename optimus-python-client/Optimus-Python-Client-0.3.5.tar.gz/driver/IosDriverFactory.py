from appium import webdriver


class IosDriverCreator(object):

    @classmethod
    def getDriver(cls, sessionUrl, desiredCapabilities):
        return webdriver.Remote(sessionUrl, desiredCapabilities)
