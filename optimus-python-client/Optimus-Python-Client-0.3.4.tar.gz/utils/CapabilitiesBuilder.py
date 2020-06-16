from json.decoder import JSONArray, JSONObject


def isBrowserAppProvided(testFeedJSON):
    try:
        testFeedJSON.getString("app")
    except Exception as error:
        print(error)
        return False
    return True


def setDesiredCapabilities(platformSpecificCapabilities, desiredCapabilities):
    keys = platformSpecificCapabilities.keys()
    while keys.hasNext():
        key = keys.next()
        if key.lower() == "app".lower():
            continue
        value = platformSpecificCapabilities.get(key)
        if isinstance(value, bool):
            desiredCapabilities.setCapability(key, platformSpecificCapabilities.getBoolean(key))
        elif isinstance(value, str):
            desiredCapabilities.setCapability(key, platformSpecificCapabilities.get(key))
        elif isinstance(value, int):
            desiredCapabilities.setCapability(key, platformSpecificCapabilities.getInt(key))
        elif isinstance(value, JSONArray):
            desiredCapabilities.setCapability(key, platformSpecificCapabilities.getJSONArray(key))


def isAndroid(testFeedJSON):
    platformName = testFeedJSON.get("platformName")
    return platformName.lower() == "Android".lower()


class CapabilitiesBuilder(object):
    capabilities = dict
    testFeedJSON = JSONObject

    def __init__(self, testFeedJSON):
        self.testFeedJSON = testFeedJSON
        appiumServerCapabilities = (testFeedJSON.get("optimusDesiredCapabilities")).get("appiumServerCapabilities")
        if not self.isNativeApp():
            self.buildWebAppCapabilities(appiumServerCapabilities)
            return
        appPath = self.getAppPath(str(testFeedJSON.get("appDir")), str(appiumServerCapabilities.get("app")))
        self.capabilities["app"] = appPath
        self.initializeCapabilities()

    def buildWebAppCapabilities(self, appiumServerCapabilities):
        appPath = self.getAppPath(str(appiumServerCapabilities["appDir"]), str(appiumServerCapabilities.get("app")))
        if isBrowserAppProvided(appiumServerCapabilities):
            self.capabilities["app"] = appPath
        self.initializeCapabilities()

    def isNativeApp(self):
        nativeApp = self.testFeedJSON.getBoolean("nativeApp")
        return nativeApp

    def initializeCapabilities(self):
        appiumServerCapabilities = (self.testFeedJSON.get("optimusDesiredCapabilities")).get("appiumServerCapabilities")
        platformSpecificCapabilities = None
        if appiumServerCapabilities.get("platformName").__str__().lower() == "Android".lower():
            platformSpecificCapabilities = (self.testFeedJSON.get("optimusDesiredCapabilities")).get(
                "androidOnlyCapabilities")
        elif appiumServerCapabilities.get("platformName").__str__().lower() == "iOS".lower():
            platformSpecificCapabilities = (self.testFeedJSON.get("optimusDesiredCapabilities")).get(
                "iOSOnlyCapabilities")
        setDesiredCapabilities(appiumServerCapabilities, self.capabilities)
        setDesiredCapabilities(platformSpecificCapabilities, self.capabilities)

    def buildCapabilities(self):
        return self.capabilities
