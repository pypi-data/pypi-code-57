class SessionInfo(object):
    buildNo = int
    sessionsReserved = str()

    def __str__(self):
        return "{buildNo={}".format(self.buildNo) \
               + ", sessionsReserved={}".format(self.sessionsReserved) + "}"
