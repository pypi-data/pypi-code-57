# -*- coding: utf-8 -*-
#
#  This file is part of SplashSync Project.
#
#  Copyright (C) 2015-2020 Splash Sync  <www.splashsync.com>
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  For the full copyright and license information, please view the LICENSE
#  file that was distributed with this source code.
#

from splashpy import Framework
from splashpy.componants import unpack, pack
from splashpy.soap.client import SoapClient, SoapFault


class SplashClient(Framework):
    __soap_client = None

    def ping(self):
        """Ping Splash Server, No Encryption, Just Say Hello!!"""

        # Create Soap Client
        soap_client = self.__get_client()
        wsId, wsKey, wsHost = self.config().identifiers()

        # Execute Ping Request
        try:
            soap_response = soap_client.Ping(id=wsId, data="test")
        # Catch Potential Errors
        except SoapFault as fault:
            Framework.log().on_fault(fault)
            return False
        except Exception as exception:
            Framework.log().fromException(exception)
            return False

        # Decode Response
        ping_response = unpack(soap_response.children().children().children().__str__(), False)

        # Verify Response
        if ping_response is False:
            return False

        return ping_response["result"] == "1"

    def connect(self):
        """Connect Splash Server, With Encryption, Just Say Hello!!"""

        # Create Soap Client
        soap_client = self.__get_client()
        wsId, wsKey, wsHost = self.config().identifiers()
        # Execute Connect Request
        try:
            soap_response = soap_client.Connect(id=wsId, data=pack({"connect": True}))
        # Catch Potential Errors
        except SoapFault as fault:
            Framework.log().on_fault(fault)
            return False
        except Exception as exception:
            Framework.log().fromException(exception)
            return False
        # Decode Response
        connect_response = unpack(soap_response.children().children().children().__str__())

        # Verify Response
        if connect_response is False:
            return False

        return connect_response["result"] == "1"

    def file(self, request):
        """Send File Request to Splash Server"""
        # Create Soap Client
        soap_client = self.__get_client()
        wsId, wsKey, wsHost = self.config().identifiers()
        # Execute Connect Request
        try:
            soap_response = soap_client.Files(id=wsId, data=pack(request))
        # Catch Potential Errors
        except SoapFault as fault:
            Framework.log().on_fault(fault)
            return False
        except Exception as exception:
            Framework.log().fromException(exception)
            return False
        # Decode Response
        connect_response = unpack(soap_response.children().children().children().__str__())

        # Verify Response
        if connect_response is False:
            return False

        return connect_response

    def __get_client(self):
        """Build Soap Client with Host Configuration"""
        if not isinstance(self.__soap_client, SoapClient):
            wsId, wsKey, wsHost = self.config().identifiers()
            self.__soap_client = SoapClient(
                location=wsHost, ns=False, exceptions=True,
                soap_server="jetty",
                http_headers={
                    'Content-type': 'application/x-www-form-urlencoded',
                }
            )

        return self.__soap_client

    @staticmethod
    def getInstance():
        """Safe Access to Splash WebService Client"""
        wsId, wsKey, wsHost = Framework.config().identifiers()

        return SplashClient(wsId, wsKey, None, None, Framework.getClientInfo(), Framework.getServerDetails(), Framework.config())


if __name__ == "__main__":
    import sys

    client = SplashClient("ThisIsSplashWsId", "ThisIsYourEncryptionKeyForSplash")
    client.config().force_host("http://localhost:8008/")

    if '--ping' in sys.argv:
        if client.ping() is True:
            print("Ping Test =>> Success")
        else:
            print("Ping Test =>> Fail")

        client.log().to_logging()

    if '--connect' in sys.argv:
        if client.connect() is True:
            print("Connect Test =>> Success")
        else:
            print("Connect Test =>> Fail")

        client.log().to_logging()
