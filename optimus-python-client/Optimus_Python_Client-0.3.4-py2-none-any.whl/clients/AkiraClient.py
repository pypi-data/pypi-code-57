import requests

from configuration import OptimusCloudConfiguration
from entities.MandatoryCaps import MandatoryCaps
from entities.SessionReservationDetails import SessionReservationDetails


def manageSession(sessionUrl, endpoint):
    return requests.put(endpoint,
                        params={"sessionUrl": sessionUrl})


class AkiraClient:
    HOST = OptimusCloudConfiguration.OptimusCloudConfiguration.AKIRA_HOST
    RESERVE_SESSION = HOST + "/reserveSession"
    UN_RESERVE_SESSION = HOST + "/unReserveSession"
    SESSION_STATE = HOST + "/sessionState"
    SESSION_CURRENT_STATE = "/currentState"
    ENGAGE_SESSION = SESSION_STATE + "/engage"
    RELEASE_SESSION = SESSION_STATE + "/release"
    TERMINATE_SESSION = SESSION_STATE + "/terminate"
    SESSION_CAPABILITIES = HOST + "/sessionCapabilities"
    FIND_MATCHING_SESSION_HOST = HOST + "/findMatchingSession"
    WFSMBOX = HOST + "/wfsmbox"

    @classmethod
    def getSessionDetails(cls, mandatoryCaps: MandatoryCaps):
        matchingSessionDetails = requests.get(
            AkiraClient.FIND_MATCHING_SESSION_HOST,
            params={"platformName": mandatoryCaps.platformName,
                    "deviceName": mandatoryCaps.getDeviceName(),
                    "platformVersion": mandatoryCaps.getPlatformVersion(),
                    "udid": mandatoryCaps.getUdid(),
                    "buildNo": mandatoryCaps.buildNo,
                    "deviceType": mandatoryCaps.getDeviceType()
                    },
        )
        print("FindMatchingSession" + AkiraClient.FIND_MATCHING_SESSION_HOST)
        return matchingSessionDetails.text

    @classmethod
    def getCurrentSessionState(cls, sessionUrl):
        sessionStateResponse = requests \
            .put(AkiraClient.SESSION_CURRENT_STATE,
                 params={"sessionUrl": sessionUrl})
        return sessionStateResponse.content

    @classmethod
    def engageSession(cls, sessionUrl):
        manageSession(sessionUrl, AkiraClient.ENGAGE_SESSION)

    @classmethod
    def releaseSession(cls, sessionUrl):
        manageSession(sessionUrl, AkiraClient.RELEASE_SESSION)

    @classmethod
    def terminateSession(cls, sessionUrl):
        manageSession(sessionUrl, AkiraClient.TERMINATE_SESSION)

    @classmethod
    def getSessionCapabilities(cls, sessionUrl):
        sessionCapabilitiesResponse = requests.get(
            AkiraClient.SESSION_CAPABILITIES,
            params={"sessionUrl": sessionUrl})
        return sessionCapabilitiesResponse.__dict__

    @classmethod
    def reserveSessions(cls, sessionReservationDetails):
        requests.post(
            AkiraClient.SESSION_CAPABILITIES,
            data={sessionReservationDetails})
        return SessionReservationDetails.__dict__

    @classmethod
    def unReserveSession(cls, buildNo):
        requests.post(
            AkiraClient.UN_RESERVE_SESSION,
            params={"buildNo", buildNo}
        )
