from bs4 import BeautifulSoup
import requests
import socket
import logging

logger = logging.getLogger(__name__)

HOME_PAGE = "/home.htm"
PROTOCOL = "http://"
TIMEOUT = 5
CONTROL_PORT = 41794

ATTRIBUTES = {
    "Status:": "STATUS",
    "Lamp Hours:": "LAMP_HOURS"
}

COMANDS = { 
	"on": [0x05, 0x00, 0x06, 0x00, 0x00, 0x03, 0x00, 0x04, 0x00],
	"off": [0x05, 0x00, 0x06, 0x00, 0x00, 0x03, 0x00, 0x05, 0x00]
}


class Projector:
    def __init__(self, host):
        self._host = host

    def __callProjectorRest(self):
        base_url = PROTOCOL + self._host
        request_url = base_url + HOME_PAGE
        
        # use requests.session since we have to get the ATOP cookie to authenticate the calls
        session = requests.Session()
        try:
            # Gets the session cookie
            session.get(base_url, timeout=TIMEOUT)

            # call the api
            logger.error("Calling home page")
            response = session.get(request_url, timeout=TIMEOUT)
            return response
        except Exception:
            logger.error("Failed to connect to projector '%s'", self._host)
            return None

    def __callProjectorSocket(self, data):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.error(bytes(data))
        try:
            s.connect((self._host, CONTROL_PORT))
            s.send(bytes(data))
        finally:
            s.close()

    def __parseResponse(self, response):
        parsedAttributes = {}
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table')[0]
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            attr = columns[0].text
            if attr in ATTRIBUTES:
                    value = columns[1].text
                    parsedAttributes[ATTRIBUTES[attr]] = value.strip()
        return parsedAttributes

    def getStatus(self):
        statusResponse = self.__callProjectorRest()
        if (statusResponse == None):
            return None

        attributes = self.__parseResponse(statusResponse)
        return {
            "state": attributes["STATUS"] != "Standby",
            "attributes": attributes
        }

    def turnOn(self):
        logger.info("Turning on projector")
        self.__callProjectorSocket(COMANDS["on"])

    def turnOff(self):
        logger.info("Turning off projector")
        self.__callProjectorSocket(COMANDS["off"])