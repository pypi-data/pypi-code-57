import json
from venv import logger

from atomos import atomic
from retrying import retry
from selenium.common.exceptions import SessionNotCreatedException

from clients.AkiraClient import AkiraClient
from driver.DriverCreatorFactory import DriverCreatorFactory
from driver.SessionManager import isSessionUp
from entities.MobileDriverDetails import MobileDriverDetails
from entities.SessionDetails import SessionDetails
from exceptions.EmptySessionUrlException import EmptySessionUrlException
from utils import CapToManCapConverter


class OptimusCloudDriver:

    def __init__(self):
        self.akiraClient = AkiraClient()

    def createDriver(self, buildNo=None, desiredCapabilities=None):
        # if testFeed is None:
        print("Creating driver with capabilities = {0}".format(
            desiredCapabilities))
        mandatoryCaps = CapToManCapConverter.convert(
            buildNo, desiredCapabilities=desiredCapabilities)
        # if desiredCapabilities is None:
        #     mandatoryCaps = TestFeedToDesiredCapConverter(testFeed).convert()
        sessionDetails = self.getSessionDetailsFromCloud(mandatoryCaps)
        print("Session details = {0}".format(sessionDetails))
        return self.initDriver(desiredCapabilities, sessionDetails)

    # def getSessionDetailsIfSessionIsUnAssigned(self, buildNo, sessionDetails):
    #     if sessionDetails.sessionUrl is None:
    #         sessionUrl = self.waitTillSessionIsAvailable(buildNo)
    #     else:
    #         return sessionDetails
    #     sessionCapabilities = self.akiraClient.getSessionCapabilities(sessionUrl)
    #     sessionDetailsUpdated = SessionDetails()
    #     sessionDetails.sessionUrl = sessionUrl
    #     sessionDetails.desiredCapabilities = sessionCapabilities
    #     sessionDetails.isReserved = True
    #     sessionDetails.sessionState = SessionState.AVAILABLE
    #     return sessionDetailsUpdated

    def initDriver(self, desiredCapabilities, sessionDetails):
        try:
            return self.getDriverDetails(desiredCapabilities, sessionDetails)
        except SessionNotCreatedException as error:
            self.akiraClient.terminateSession(sessionDetails.sessionUrl)
            logger.error(error)
            raise Exception('Cannot initialize driver')

    # def waitTillSessionIsAvailable(self, buildNo):
    #     sessionUrl = ""
    #     sessionQueueReader = SessionQueueReader()
    #     isMessageRead = False
    #     while not isMessageRead:
    #         poll(
    #             lambda: queueHasAMessage(buildNo),
    #             timeout=120,
    #             step=5
    #         )
    #         sessionUrl = consumeMessage(buildNo)
    #         if sessionUrl is None or not sessionUrl:
    #             isMessageRead = True
    #             self.akiraClient.engageSession(sessionUrl)
    #     return sessionUrl

    @staticmethod
    def getMobileDriverDetails(
            sessionDetails: SessionDetails(),
            desiredCapabilities,
            mobileDriver):
        mobileDriverDetails = MobileDriverDetails()
        mobileDriverDetails.sessionUrl = (sessionDetails.get("sessionUrl"))
        mobileDriverDetails.mobileDriver = mobileDriver
        mobileDriverDetails.udid = (
            sessionDetails.get("desiredCapabilities").get("udid"))
        mobileDriverDetails.desiredCapabilities = desiredCapabilities
        return mobileDriverDetails

    @classmethod
    def getDesiredCapabilities(cls, desiredCapabilities: dict):
        desiredCapabilities1 = {}
        for key, value in desiredCapabilities.items():
            desiredCapabilities1[key] = value
        return desiredCapabilities1

    @retry(stop_max_attempt_number=100, wait_fixed=4000)
    def getSessionDetailsFromCloud(self, mandatoryCaps):
        sessionDetails = atomic.AtomicReference(SessionDetails)
        try:
            sessionDetails.set(
                self.akiraClient.getSessionDetails(mandatoryCaps))
            print("Mandatory caps ={}".format(mandatoryCaps))
            print("Session details ={}".format(sessionDetails.get()))
            sessionDetail = json.loads(sessionDetails.get())
            sessionUrl = sessionDetail.get("sessionUrl")
            if sessionUrl is None:
                raise EmptySessionUrlException()
            sessionUp = isSessionUp(sessionUrl)
            if not sessionUp:
                self.akiraClient.terminateSession(sessionUrl)
                raise EmptySessionUrlException()
            return sessionDetail
        except Exception as error:
            print(error)
            raise print("Retrying session")

    @retry(stop_max_attempt_number=100)
    def getDriverDetails(self, desiredCapabilities, sessionDetails):
        for key, value in sessionDetails.get("desiredCapabilities").items():
            desiredCapabilities[key] = value
        mobileDriver = DriverCreatorFactory().getInstance(
            sessionDetails.get("sessionUrl"), desiredCapabilities)
        return self.getMobileDriverDetails(
            sessionDetails, desiredCapabilities, mobileDriver)
