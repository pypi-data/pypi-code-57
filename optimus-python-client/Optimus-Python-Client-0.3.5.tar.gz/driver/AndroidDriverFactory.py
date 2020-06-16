from appium import webdriver


class AndroidDriverCreator(object):

    @classmethod
    def getDriver(cls, sessionUrl, desiredCapabilities):
        print("sessionUrl - " + sessionUrl)
        return webdriver.Remote(sessionUrl, desiredCapabilities)
