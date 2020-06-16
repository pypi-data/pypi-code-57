from entities.SessionState import SessionState


class SessionDetails(object):
    desiredCapabilities = {}
    sessionUrl = str()
    sessionState = SessionState()
    isReserved = str()

    def __str__(self):
        return "{" + "desiredCapabilities={}".format(self.desiredCapabilities) \
               + ", sessionUrl={}".format(self.sessionUrl) \
               + ", sessionState={}".format(self.sessionState) \
               + ", isReserved={}".format(self.isReserved) + "}"
