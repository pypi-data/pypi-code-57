from appium import webdriver


class MobileDriverDetails(object):
    mobileDriver = webdriver.Remote
    sessionUrl = str

    # For Optimus Usage
    udid = str

    # For dashboard usage
    desiredCapabilities = {}
