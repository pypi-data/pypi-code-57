class MandatoryCaps(object):
    def __init__(self):
        self.platformName = str()
        self.deviceName = str
        self.deviceType = str()
        self.platformVersion = str()
        self.udId = str
        self.buildNo = str()

    def getDeviceName(self):
        if self.deviceName == 'None':
            return ''

    def getDeviceType(self):
        if self.deviceType == 'None':
            return ''

    def getPlatformVersion(self):
        if self.platformVersion == 'None':
            return ''

    def getUdid(self):
        if self.udId == 'None':
            return ''

    def __str__(self):
        return " platformName={}".format(self.platformName) \
               + ",deviceName={}".format(MandatoryCaps.getDeviceName(self)) \
               + " ,deviceType={}".format(MandatoryCaps.getDeviceType(self)) \
               + " ,platformVersion={}".format(MandatoryCaps.getPlatformVersion(self)) \
               + " ,udid={}".format(MandatoryCaps.getUdid(self)) \
               + " ,buildNo={}".format(self.buildNo)
