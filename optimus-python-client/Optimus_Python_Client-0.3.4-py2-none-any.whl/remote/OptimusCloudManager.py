from clients.AkiraClient import AkiraClient
from entities.SessionInfo import SessionInfo
from entities.SessionReservationDetails import SessionReservationDetails
from entities.SessionsByPlatform import SessionsByPlatform
from utils.BuildNoGenerator import BuildNoGenerator

class OptimusCloudManager(object):
    akiraClient: AkiraClient

    def __int__(self):
        self.akiraClient = AkiraClient()

    @classmethod
    def getBuildNo(cls, buildNo):
        if buildNo is None:
            return BuildNoGenerator().getBuildNo()
        else:
            return buildNo

    def reserveSession(
            self,
            buildNo,
            numOfSessionsToBeReserved,
            platformsToBeReserved):
        buildNo = self.getBuildNo(buildNo)
        sessionReservationDetails = SessionReservationDetails()
        sessionReservationDetails.setBuildNo = buildNo
        sessionsByPlatform = SessionsByPlatform()
        sessionsByPlatform.platformName = platformsToBeReserved
        sessionsByPlatform.sessionsRequired = numOfSessionsToBeReserved
        sessionReservationDetails.sessionDetails = sessionsByPlatform
        sessionsReserved = akiraClient.reserveSessions(
            sessionReservationDetails)
        sessionInfo = SessionInfo()
        sessionInfo.buildNo = buildNo
        sessionInfo.sessionsReserved = sessionsReserved.totalSessions
        return sessionInfo

    def reserveAndroidSession(
            self,
            buildNo=None,
            numOfAndroidSessionsToBeReserved=None):
        return self.reserveSession(
            buildNo, numOfAndroidSessionsToBeReserved, "Android")

    def reserveIosSession(
            self,
            buildNo=None,
            numOfAndroidSessionsToBeReserved=None):
        return self.reserveSession(
            buildNo, numOfAndroidSessionsToBeReserved, "IOS")

    def getSessionsByPlatform(self, platformName, numOfSessionsToBeReserved):
        sessionsByPlatform = SessionsByPlatform()
        sessionsByPlatform.platformName = platformName
        sessionsByPlatform.sessionsRequired = numOfSessionsToBeReserved
        return sessionsByPlatform

    def reserveAndroidAndIosSessions(
            self,
            noOfAndroidSessions,
            noOfIOSSessions,
            buildNo=None,
    ):
        buildNo = self.getBuildNo(buildNo)
        sessionReservationDetails = SessionReservationDetails()
        sessionReservationDetails.setBuildNo = buildNo
        androidSession = self.getSessionsByPlatform(
            "Android", noOfAndroidSessions)
        iOSSession = self.getSessionsByPlatform("IOS", noOfIOSSessions)
        SessionReservationDetails.sessionDetails = [androidSession, iOSSession]
        return akiraClient.reserveSessions(sessionReservationDetails)

    @classmethod
    def unReserveSession(cls, buildNo):
        akiraClient.unReserveSession(buildNo)

    @classmethod
    def engageSession(cls, sessionUrl):
        return akiraClient.engageSession(sessionUrl)

    @classmethod
    def releaseSession(cls, mobileDriverDetails):
        return akiraClient.releaseSession(mobileDriverDetails.sessionUrl)

    @classmethod
    def terminateSession(cls, sessionUrl):
        akiraClient.terminateSession(sessionUrl)

    @classmethod
    def getSessionState(cls, sessionUrl):
        return akiraClient.getCurrentSessionState(sessionUrl)
