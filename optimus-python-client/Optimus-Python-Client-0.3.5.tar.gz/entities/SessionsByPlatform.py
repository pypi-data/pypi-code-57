class SessionsByPlatform(object):
    platformName = str
    sessionsRequired = int
    sessionsAllocated = int

    def __str__(self):
        return "{platformName={}".format(self.platformName) + \
               ", sessionsRequired={}".format(self.sessionsRequired) + \
               ", sessionsAllocated={}".format(self.sessionsAllocated) + '}'
