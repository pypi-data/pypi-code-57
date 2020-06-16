from entities.MandatoryCaps import MandatoryCaps


def convert(buildNo, desiredCapabilities):
    mandatoryCaps = MandatoryCaps()
    mandatoryCaps.buildNo = buildNo
    mandatoryCaps.platformName = desiredCapabilities.get("platformName")
    mandatoryCaps.platformVersion = desiredCapabilities.get("platformVersion")
    mandatoryCaps.deviceType = desiredCapabilities.get("deviceType")
    mandatoryCaps.udId = desiredCapabilities.get("udid")
    mandatoryCaps.deviceName = desiredCapabilities.get("deviceName")
    return mandatoryCaps


class CapToManCapConverter(object):
    pass
